import os

from . import autogenerate as autogen
from . import util
from .runtime.environment import EnvironmentContext
from .script import ScriptDirectory


def list_templates(config):
    """List available templates.

    :param config: a :class:`.Config` object.

    """

    config.print_stdout("Available templates:\n")
    for tempname in os.listdir(config.get_template_directory()):
        with open(
            os.path.join(config.get_template_directory(), tempname, "README")
        ) as readme:
            synopsis = next(readme)
        config.print_stdout("%s - %s", tempname, synopsis)

    config.print_stdout("\nTemplates are used via the 'init' command, e.g.:")
    config.print_stdout("\n  alembic init --template generic ./scripts")


def init(config, directory, template="generic", package=False):
    """Initialize a new scripts directory.

    :param config: a :class:`.Config` object.

    :param directory: string path of the target directory

    :param template: string name of the migration environment template to
     use.

    :param package: when True, write ``__init__.py`` files into the
     environment location as well as the versions/ location.

     .. versionadded:: 1.2


    """

    if os.access(directory, os.F_OK) and os.listdir(directory):
        raise util.CommandError(
            "Directory %s already exists and is not empty" % directory
        )

    template_dir = os.path.join(config.get_template_directory(), template)
    if not os.access(template_dir, os.F_OK):
        raise util.CommandError("No such template %r" % template)

    if not os.access(directory, os.F_OK):
        util.status(
            "Creating directory %s" % os.path.abspath(directory),
            os.makedirs,
            directory,
        )

    versions = os.path.join(directory, "versions")
    util.status(
        "Creating directory %s" % os.path.abspath(versions),
        os.makedirs,
        versions,
    )

    script = ScriptDirectory(directory)

    for file_ in os.listdir(template_dir):
        file_path = os.path.join(template_dir, file_)
        if file_ == "alembic.ini.mako":
            config_file = os.path.abspath(config.config_file_name)
            if os.access(config_file, os.F_OK):
                util.msg("File %s already exists, skipping" % config_file)
            else:
                script._generate_template(
                    file_path, config_file, script_location=directory
                )
        elif os.path.isfile(file_path):
            output_file = os.path.join(directory, file_)
            script._copy_file(file_path, output_file)

    if package:
        for path in [
            os.path.join(os.path.abspath(directory), "__init__.py"),
            os.path.join(os.path.abspath(versions), "__init__.py"),
        ]:
            file_ = util.status("Adding %s" % path, open, path, "w")
            file_.close()

    util.msg(
        "Please edit configuration/connection/logging "
        "settings in %r before proceeding." % config_file
    )


def revision(
    config,
    message=None,
    autogenerate=False,
    sql=False,
    head="head",
    splice=False,
    branch_label=None,
    version_path=None,
    rev_id=None,
    depends_on=None,
    process_revision_directives=None,
):
    """Create a new revision file.

    :param config: a :class:`.Config` object.

    :param message: string message to apply to the revision; this is the
     ``-m`` option to ``alembic revision``.

    :param autogenerate: whether or not to autogenerate the script from
     the database; this is the ``--autogenerate`` option to
     ``alembic revision``.

    :param sql: whether to dump the script out as a SQL string; when specified,
     the script is dumped to stdout.  This is the ``--sql`` option to
     ``alembic revision``.

    :param head: head revision to build the new revision upon as a parent;
     this is the ``--head`` option to ``alembic revision``.

    :param splice: whether or not the new revision should be made into a
     new head of its own; is required when the given ``head`` is not itself
     a head.  This is the ``--splice`` option to ``alembic revision``.

    :param branch_label: string label to apply to the branch; this is the
     ``--branch-label`` option to ``alembic revision``.

    :param version_path: string symbol identifying a specific version path
     from the configuration; this is the ``--version-path`` option to
     ``alembic revision``.

    :param rev_id: optional revision identifier to use instead of having
     one generated; this is the ``--rev-id`` option to ``alembic revision``.

    :param depends_on: optional list of "depends on" identifiers; this is the
     ``--depends-on`` option to ``alembic revision``.

    :param process_revision_directives: this is a callable that takes the
     same form as the callable described at
     :paramref:`.EnvironmentContext.configure.process_revision_directives`;
     will be applied to the structure generated by the revision process
     where it can be altered programmatically.   Note that unlike all
     the other parameters, this option is only available via programmatic
     use of :func:`.command.revision`

     .. versionadded:: 0.9.0

    """

    script_directory = ScriptDirectory.from_config(config)

    command_args = dict(
        message=message,
        autogenerate=autogenerate,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
        depends_on=depends_on,
    )
    revision_context = autogen.RevisionContext(
        config,
        script_directory,
        command_args,
        process_revision_directives=process_revision_directives,
    )

    environment = util.asbool(config.get_main_option("revision_environment"))

    if autogenerate:
        environment = True

        if sql:
            raise util.CommandError(
                "Using --sql with --autogenerate does not make any sense"
            )

        def retrieve_migrations(rev, context):
            revision_context.run_autogenerate(rev, context)
            return []

    elif environment:

        def retrieve_migrations(rev, context):
            revision_context.run_no_autogenerate(rev, context)
            return []

    elif sql:
        raise util.CommandError(
            "Using --sql with the revision command when "
            "revision_environment is not configured does not make any sense"
        )

    if environment:
        with EnvironmentContext(
            config,
            script_directory,
            fn=retrieve_migrations,
            as_sql=sql,
            template_args=revision_context.template_args,
            revision_context=revision_context,
        ):
            script_directory.run_env()

        # the revision_context now has MigrationScript structure(s) present.
        # these could theoretically be further processed / rewritten *here*,
        # in addition to the hooks present within each run_migrations() call,
        # or at the end of env.py run_migrations_online().

    scripts = [script for script in revision_context.generate_scripts()]
    if len(scripts) == 1:
        return scripts[0]
    else:
        return scripts


def merge(config, revisions, message=None, branch_label=None, rev_id=None):
    """Merge two revisions together.  Creates a new migration file.

    .. versionadded:: 0.7.0

    :param config: a :class:`.Config` instance

    :param message: string message to apply to the revision

    :param branch_label: string label name to apply to the new revision

    :param rev_id: hardcoded revision identifier instead of generating a new
     one.

    .. seealso::

        :ref:`branches`

    """

    script = ScriptDirectory.from_config(config)
    template_args = {
        "config": config  # Let templates use config for
        # e.g. multiple databases
    }
    return script.generate_revision(
        rev_id or util.rev_id(),
        message,
        refresh=True,
        head=revisions,
        branch_labels=branch_label,
        **template_args
    )


def upgrade(config, revision, sql=False, tag=None):
    """Upgrade to a later version.

    :param config: a :class:`.Config` instance.

    :param revision: string revision target or range for --sql mode

    :param sql: if True, use ``--sql`` mode

    :param tag: an arbitrary "tag" that can be intercepted by custom
     ``env.py`` scripts via the :meth:`.EnvironmentContext.get_tag_argument`
     method.

    """

    script = ScriptDirectory.from_config(config)

    starting_rev = None
    if ":" in revision:
        if not sql:
            raise util.CommandError("Range revision not allowed")
        starting_rev, revision = revision.split(":", 2)

    def upgrade(rev, context):
        return script._upgrade_revs(revision, rev)

    with EnvironmentContext(
        config,
        script,
        fn=upgrade,
        as_sql=sql,
        starting_rev=starting_rev,
        destination_rev=revision,
        tag=tag,
    ):
        script.run_env()


def downgrade(config, revision, sql=False, tag=None):
    """Revert to a previous version.

    :param config: a :class:`.Config` instance.

    :param revision: string revision target or range for --sql mode

    :param sql: if True, use ``--sql`` mode

    :param tag: an arbitrary "tag" that can be intercepted by custom
     ``env.py`` scripts via the :meth:`.EnvironmentContext.get_tag_argument`
     method.

    """

    script = ScriptDirectory.from_config(config)
    starting_rev = None
    if ":" in revision:
        if not sql:
            raise util.CommandError("Range revision not allowed")
        starting_rev, revision = revision.split(":", 2)
    elif sql:
        raise util.CommandError(
            "downgrade with --sql requires <fromrev>:<torev>"
        )

    def downgrade(rev, context):
        return script._downgrade_revs(revision, rev)

    with EnvironmentContext(
        config,
        script,
        fn=downgrade,
        as_sql=sql,
        starting_rev=starting_rev,
        destination_rev=revision,
        tag=tag,
    ):
        script.run_env()


def show(config, rev):
    """Show the revision(s) denoted by the given symbol.

    :param config: a :class:`.Config` instance.

    :param revision: string revision target

    """

    script = ScriptDirectory.from_config(config)

    if rev == "current":

        def show_current(rev, context):
            for sc in script.get_revisions(rev):
                config.print_stdout(sc.log_entry)
            return []

        with EnvironmentContext(config, script, fn=show_current):
            script.run_env()
    else:
        for sc in script.get_revisions(rev):
            config.print_stdout(sc.log_entry)


def history(config, rev_range=None, verbose=False, indicate_current=False):
    """List changeset scripts in chronological order.

    :param config: a :class:`.Config` instance.

    :param rev_range: string revision range

    :param verbose: output in verbose mode.

    :param indicate_current: indicate current revision.

     ..versionadded:: 0.9.9

    """

    script = ScriptDirectory.from_config(config)
    if rev_range is not None:
        if ":" not in rev_range:
            raise util.CommandError(
                "History range requires [start]:[end], " "[start]:, or :[end]"
            )
        base, head = rev_range.strip().split(":")
    else:
        base = head = None

    environment = (
        util.asbool(config.get_main_option("revision_environment"))
        or indicate_current
    )

    def _display_history(config, script, base, head, currents=()):
        for sc in script.walk_revisions(
            base=base or "base", head=head or "heads"
        ):

            if indicate_current:
                sc._db_current_indicator = sc.revision in currents

            config.print_stdout(
                sc.cmd_format(
                    verbose=verbose,
                    include_branches=True,
                    include_doc=True,
                    include_parents=True,
                )
            )

    def _display_history_w_current(config, script, base, head):
        def _display_current_history(rev, context):
            if head == "current":
                _display_history(config, script, base, rev, rev)
            elif base == "current":
                _display_history(config, script, rev, head, rev)
            else:
                _display_history(config, script, base, head, rev)
            return []

        with EnvironmentContext(config, script, fn=_display_current_history):
            script.run_env()

    if base == "current" or head == "current" or environment:
        _display_history_w_current(config, script, base, head)
    else:
        _display_history(config, script, base, head)


def heads(config, verbose=False, resolve_dependencies=False):
    """Show current available heads in the script directory.

    :param config: a :class:`.Config` instance.

    :param verbose: output in verbose mode.

    :param resolve_dependencies: treat dependency version as down revisions.

    """

    script = ScriptDirectory.from_config(config)
    if resolve_dependencies:
        heads = script.get_revisions("heads")
    else:
        heads = script.get_revisions(script.get_heads())

    for rev in heads:
        config.print_stdout(
            rev.cmd_format(
                verbose, include_branches=True, tree_indicators=False
            )
        )


def branches(config, verbose=False):
    """Show current branch points.

    :param config: a :class:`.Config` instance.

    :param verbose: output in verbose mode.

    """
    script = ScriptDirectory.from_config(config)
    for sc in script.walk_revisions():
        if sc.is_branch_point:
            config.print_stdout(
                "%s\n%s\n",
                sc.cmd_format(verbose, include_branches=True),
                "\n".join(
                    "%s -> %s"
                    % (
                        " " * len(str(sc.revision)),
                        rev_obj.cmd_format(
                            False, include_branches=True, include_doc=verbose
                        ),
                    )
                    for rev_obj in (
                        script.get_revision(rev) for rev in sc.nextrev
                    )
                ),
            )


def current(config, verbose=False, head_only=False):
    """Display the current revision for a database.

    :param config: a :class:`.Config` instance.

    :param verbose: output in verbose mode.

    :param head_only: deprecated; use ``verbose`` for additional output.

    """

    script = ScriptDirectory.from_config(config)

    if head_only:
        util.warn("--head-only is deprecated", stacklevel=3)

    def display_version(rev, context):
        if verbose:
            config.print_stdout(
                "Current revision(s) for %s:",
                util.obfuscate_url_pw(context.connection.engine.url),
            )
        for rev in script.get_all_current(rev):
            config.print_stdout(rev.cmd_format(verbose))

        return []

    with EnvironmentContext(config, script, fn=display_version):
        script.run_env()


def stamp(config, revision, sql=False, tag=None, purge=False):
    """'stamp' the revision table with the given revision; don't
    run any migrations.

    :param config: a :class:`.Config` instance.

    :param revision: target revision or list of revisions.   May be a list
     to indicate stamping of multiple branch heads.

     .. note:: this parameter is called "revisions" in the command line
        interface.

     .. versionchanged:: 1.2  The revision may be a single revision or
        list of revisions when stamping multiple branch heads.

    :param sql: use ``--sql`` mode

    :param tag: an arbitrary "tag" that can be intercepted by custom
     ``env.py`` scripts via the :class:`.EnvironmentContext.get_tag_argument`
     method.

    :param purge: delete all entries in the version table before stamping.

     .. versionadded:: 1.2

    """

    script = ScriptDirectory.from_config(config)

    if sql:
        destination_revs = []
        starting_rev = None
        for _revision in util.to_list(revision):
            if ":" in _revision:
                srev, _revision = _revision.split(":", 2)

                if starting_rev != srev:
                    if starting_rev is None:
                        starting_rev = srev
                    else:
                        raise util.CommandError(
                            "Stamp operation with --sql only supports a "
                            "single starting revision at a time"
                        )
            destination_revs.append(_revision)
    else:
        destination_revs = util.to_list(revision)

    def do_stamp(rev, context):
        return script._stamp_revs(util.to_tuple(destination_revs), rev)

    with EnvironmentContext(
        config,
        script,
        fn=do_stamp,
        as_sql=sql,
        starting_rev=starting_rev if sql else None,
        destination_rev=util.to_tuple(destination_revs),
        tag=tag,
        purge=purge,
    ):
        script.run_env()


def edit(config, rev):
    """Edit revision script(s) using $EDITOR.

    :param config: a :class:`.Config` instance.

    :param rev: target revision.

    """

    script = ScriptDirectory.from_config(config)

    if rev == "current":

        def edit_current(rev, context):
            if not rev:
                raise util.CommandError("No current revisions")
            for sc in script.get_revisions(rev):
                util.edit(sc.path)
            return []

        with EnvironmentContext(config, script, fn=edit_current):
            script.run_env()
    else:
        revs = script.get_revisions(rev)
        if not revs:
            raise util.CommandError(
                "No revision files indicated by symbol '%s'" % rev
            )
        for sc in revs:
            util.edit(sc.path)
