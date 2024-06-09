from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType
import requests
from django.conf import settings
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView



class TodoListApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        spark = SparkSession.builder.appName('test').getOrCreate()
        # schema = 'Age INTEGER, Sex STRING, ChestPainType STRING'
        df = spark.read.csv('heart.csv', inferSchema=True, header=True)
        # df = spark.read.csv('heart.csv', nullValue='NA') replace nulls with other value at reading time
        # df.write.format("csv").mode("overwrite").save("heart_save.csv") if you want to overwrite the file
        # df.select(['Age','Sex']).show(3)
        # df.cache()
        # df.collect()
        df = df.withColumn("Age", df.Age.cast(FloatType()))
        df = df.withColumn("RestingBP", df.RestingBP.cast(FloatType()))
        df.select(['Age','RestingBP']).describe().show()
        return Response(data={'asdasd':'wqqwe'}, status=status.HTTP_200_OK)
    

    
class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter


class CheckAuthenticatedUser(APIView):
    
    def get(self, request):
        response = 'user already authenticated'
        if not request.user.is_authenticated:
            github_client_id = settings.SOCIALACCOUNT_PROVIDERS['github']['APP']['client_id']
            response = f'https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri=http://{settings.BACKEND_URL}/aws-api/login_github_user_token&scope=user'
            
        return Response(data={'redirect_url':response}, status=status.HTTP_200_OK)
    

class OAuthLoginGithubUser(APIView):
    
    def get(self, request):
            github_client_id = settings.SOCIALACCOUNT_PROVIDERS['github']['APP']['client_id']
            github_client_secret = settings.SOCIALACCOUNT_PROVIDERS['github']['APP']['secret']
            code_from_github = request.GET.get('code')
            response = requests.get(f'https://github.com/login/oauth/access_token?client_id={github_client_id}&client_secret={github_client_secret}&code={code_from_github}')
            response = requests.post(f'{settings.BACKEND_URL}/aws-api/github', data ={'key':response.access_token}) # This POST request to the Github View will set the Django Token for the User in the database and also return that Token in response.
            return Response(data={'access_token':response.access_token}, status=status.HTTP_200_OK)
        