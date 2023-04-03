from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework.views import APIView, Response, Request, status
from teams.models import Team
from teams.utils import data_processing
from teams.exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError

# Create your views here.
class TeamView(APIView):
    def post(self, request: Request):
        must_contain_keys = ("name", "titles", "top_scorer", "fifa_code", "first_cup")

        for key in tuple(dict.keys(request.data)):
            if key not in must_contain_keys:
                request.data.pop(key)
            
        for must_key in must_contain_keys:
            if must_key not in tuple(dict.keys(request.data)):
                return Response({"error": f"Missing {must_key}"}, status.HTTP_400_BAD_REQUEST)

        teams = Team.objects.filter(fifa_code = request.data["fifa_code"])

        try:
            data_processing(request.data)
        except (ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError) as error:
            return Response({"error": error.message}, status.HTTP_400_BAD_REQUEST)

        if len(teams) > 0:
            return Response({"msg": f"Fifa code already exists."}, status.HTTP_409_CONFLICT)
            
        created_item = Team.objects.create(**request.data)
        translate = model_to_dict(created_item)

        return Response(translate, status.HTTP_201_CREATED)
    
    def get(self, request: Request):
        get_response = Team.objects.all()
        teams = [model_to_dict(team) for team in get_response]
        
        return Response(teams, status.HTTP_200_OK)
    
class TeamIdView(APIView):
    def patch(self, request: Request, team_id):
        find_team = Team.objects.filter(id = team_id)
        if not len(find_team) > 0:
                    return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        if not dict.keys(request.data):
            return Response({"message": "No body found."}, status.HTTP_400_BAD_REQUEST)
        
        possible_keys = ("name", "titles", "top_scorer", "fifa_code", "first_cup")

        for key in tuple(dict.keys(request.data)):
            if key not in possible_keys:
                request.data.pop(key)

        for index, key in enumerate(request.data):
            setattr(find_team[0], key, request.data[key])
        find_team[0].save()
    
        return Response(model_to_dict(find_team[0]), status.HTTP_200_OK)

    def delete(self, request: Request, team_id):
        find_team = Team.objects.filter(id = team_id)
        if not len(find_team) > 0:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        find_team[0].delete()

        return Response(None, status.HTTP_204_NO_CONTENT)
    
    def get(self, request: Request, team_id):
        find_team = Team.objects.filter(id = team_id)
        if not len(find_team) > 0:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)
        
        return Response(model_to_dict(find_team[0]), status.HTTP_200_OK)