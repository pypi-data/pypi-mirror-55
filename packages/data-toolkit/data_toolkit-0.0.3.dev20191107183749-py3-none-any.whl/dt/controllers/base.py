
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from ..ext.tracking import tracking
from ..ext.config_cmd import config

VERSION_BANNER = """
ML & data helper code! %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'ML & data helper code!'

        # text displayed at the bottom of --help output
        epilog = 'Usage: dt command1 --foo bar'

        # controller level arguments. ex: 'dt --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    @ex(
        help='example sub command1',

        # sub-command level arguments. ex: 'dt command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-f', '--foo' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'foo' } ),
        ],
    )
    def command1(self):
        """Example sub-command."""

        data = {
            'foo' : 'bar',
        }

        ### do something with arguments
        if self.app.pargs.foo is not None:
            data['foo'] = self.app.pargs.foo

        self.app.render(data, 'command1.jinja2')

    @ex(
        help='Operations with config.',
        arguments = [
            (['show'], {
                "help" : 'Show configs: Sentry DNS etc.',
                'action' : "store"
            })
        ]
    )
    def config(self):
        args = self.app.pargs
        if args.show is not None:
            for attr in dir(config):
                if not attr.startswith('_'):
                    print(f"{attr}: {getattr(config,attr)}")

    @ex(
        help='Tracks your ML code till finish',
        arguments=[
            (['flags'], {
                'help' : 'Which flags you want to pass to the underlying script.'
                         'e.g. --parallel --batch_size 256',
                'action' : "store"
            }),
            (['-ns'], {    
            'help' : 'Shuts down the computer between in the shutdown_hours.'
                      'Set to 22-08. Default: True',
            "action" : 'store'
            }),
            (['-t'], {
                'help' : 'If we are testing / doing a dry run. Default: False',
                "action" : "store"
            }),
            (['-cfg'],{
                'help': "location of the config file",
                "action" : "store",
            }),
            (['-p'],{
                "help": "which Python interpreter to use."
                        " Default is determined by `which python3`",
                "action" : "store"
            })
        ]
    )

    def track(self):
        ''' 'Tracks experiments by making a Sentry alert when a script finishes. ''' 
        args = self.app.pargs
        if self.app.pargs is not None:
            tracking(args.flags, args.t, args.ns, args.p)