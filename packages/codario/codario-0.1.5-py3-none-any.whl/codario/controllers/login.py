from cement import Controller, ex, shell
import urllib3, json, getpass

class Login(Controller):
    class Meta:
        label = 'login'
        stacked_type = 'embedded'
        stacked_on = 'base'

    @ex(
        help='Login with your account.',
        arguments=[
            (
                [ '--email' ],
                {
                    'help' : 'Your email.',
                    'action' : 'store',
                    'dest' : 'email'
                }
            ),
            (
                [ '--password' ],
                {
                    'help' : 'Your password.',
                    'action' : 'store',
                    'dest' : 'password'
                }
            ),
        ]
    )
    def login(self):
        data = {
            '_username' : self.app.pargs.email,
            'password' : self.app.pargs.password,
        }

        if data['_username'] is None:
            p = shell.Prompt('Type your email:', default=None)
            promptString = p.prompt()
            data['_username'] = promptString

        if data['password'] is None:
            promptString = getpass.getpass(prompt='Type your password:')
            data['password'] = promptString

        http = urllib3.PoolManager()

        encoded_data = json.dumps(data).encode('utf-8')

        r = http.request('POST', 'https://api.codario.io/login/check', body=encoded_data)

        response = json.loads(r.data.decode('utf-8'))

        if response['success']:
            self.app.log.success('You are authorized now to use the Codario CLI tool.')

            self.app.db.table('tokens').purge()
            self.app.db.table('tokens').insert(response)
        else:
            self.app.log.error('The email or password that you have entered is incorrect.')
