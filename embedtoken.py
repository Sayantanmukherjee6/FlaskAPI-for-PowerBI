import requests

class EmbedToken:
    def __init__(self,access_token,username,password,client_id,client_secret,report_id,group_id,settings=None):
        self.access_token = access_token
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret= client_secret
        self.report_id = report_id
        self.group_id= group_id
        if settings is None:
            self.settings = {'accessLevel': 'View', 'allowSaveAs': 'false'}
        else:
            self.settings = settings        
        self.config = self.get_embed_token()

    def get_embed_token(self):
        dest = 'https://api.powerbi.com/v1.0/myorg/groups/' + self.group_id \
               + '/reports/' + self.report_id + '/GenerateToken'
        embed_url = 'https://app.powerbi.com/reportEmbed?reportId=' \
                    + self.report_id + '&groupId=' + self.group_id

        print self.access_token
        headers = {'Authorization': 'Bearer ' + self.access_token}
        response = requests.post(dest, data=self.settings, headers=headers)
        self.token = response.json().get('token')
        return {'token': self.token, 'embed_url': embed_url, 'report_id': self.report_id}

    def get_report(self):
        headers = {'Authorization': 'Bearer ' + self.token}
        dest = 'https://app.powerbi.com/reportEmbed?reportId=' + self.report_id + \
               '&amp;groupId=' + self.group_id
        response = requests.get(dest, data=self.settings, headers=headers)
        return response