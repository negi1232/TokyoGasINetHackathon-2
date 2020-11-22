import json
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import EvacuationSite, DangerLocations

SEARCH_RANGE_LAT = 0.02695 # (度)
SEARCH_RANGE_LNG = 0.02695 # (度)

DANGER_TYPES = [
    'gas',
    'collapse'
]

def index(request):
    context = {}

    position = []
    dangerLocations = []
    evacuationSites = []
    goal = []
    wayPoints = []

    # begin debug
    dangerLocations = [
        [35.687, 139.7598, 'collapse'],
        [35.68551, 139.77302, 'collapse'],
        [35.67509, 139.76059, 'gas']
    ]
    # end debug


    if 'latitude' in request.GET and 'longitude' in request.GET:
        # ユーザの場所が指定されている場合
        ## positionに，指定されたユーザの位置を設定する
        position.append(
            float(request.GET.get('latitude'))
        )
        position.append(
            float(request.GET.get('longitude'))
        )

        if 'goal_latitude' in request.GET and 'goal_longitude' in request.GET:
            goal = [
                float(request.GET.get('goal_latitude')),
                float(request.GET.get('goal_longitude'))
            ]

            """
            ここでwayPointsを算出
            """
            # begin debug
            if (float(request.GET.get('goal_latitude')) == 35.679813655983 and float(request.GET.get('goal_longitude')) == 139.7769934504):
                wayPoints = [
                    [35.679478, 139.771698],
                    [35.678227, 139.774466],
                    [35.678771, 139.774856],
                    [35.679612, 139.775354],
                    [35.679349, 139.776051],
                    [35.680649, 139.776878],
                    [35.680459, 139.777466],
                    [35.67990729379566, 139.77709236026595]
                ]
            elif (float(request.GET.get('goal_latitude')) == 35.676572613649 and float(request.GET.get('goal_longitude')) == 139.77132890862):
                wayPoints = [
                    [35.679478, 139.771698],
                    [35.678510122094934, 139.77118555763727],
                    [35.677798, 139.770605],
                    [35.677109, 139.770467],
                    [35.676679, 139.771367],
                    [35.67656780468001, 139.77134018680187]
                ]
            # end debug

        ## 近くな危険な場所を設定する
        nearbyDangerLocations = DangerLocations.objects.filter(
            latitude__range=(position[0]-(SEARCH_RANGE_LAT/2), position[0]+(SEARCH_RANGE_LAT/2)),
            longitude__range=(position[1]-(SEARCH_RANGE_LNG/2), position[1]+(SEARCH_RANGE_LNG/2))
        )

        for dangerLocation in nearbyDangerLocations:
            dangerLocations.append([
                dangerLocation.latitude,
                dangerLocation.longitude,
                dangerLocation.dangerType
            ])

        ## 近くの避難場所の位置を設定する
        nearbyEvacuationSites = EvacuationSite.objects.filter(
            latitude__range=(position[0]-(SEARCH_RANGE_LAT/2), position[0]+(SEARCH_RANGE_LAT/2)),
            longitude__range=(position[1]-(SEARCH_RANGE_LNG/2), position[1]+(SEARCH_RANGE_LNG/2))
        )

        for evacuationSite in nearbyEvacuationSites:
            evacuationSites.append([
                evacuationSite.latitude,
                evacuationSite.longitude
            ])

    context = {
        'position':     json.dumps(position),
        'danger':       json.dumps(dangerLocations),
        'evacuation':   json.dumps(evacuationSites),
        'goal':         json.dumps(goal),
        'wayPoints':    json.dumps(wayPoints)
    }

    return render(request, 'index.html', context)

# 危険地帯登録用
def regist(request):
    response = {'status': 'OK'}
    errorMessage = ''

    # 必要な値が全てあるかどうか確認
    for q in ['latitude', 'longitude', 'danger_type', 'regist']:
        if q not in request.GET:
            errorMessage += u'{} is not specified.\n'.format(q)

    # エラーメッセージが更新されていれば、NGとして返す
    if errorMessage != '':
        response['status'] = 'NG'
        response['message'] = errorMessage

        return JsonResponse(response)

    # TODO: 以下の処理は，全ての値が正常であることを前提に行っているが，try-catchなどによるNG判定が必要

    if request.GET.get('regist') == '1':
        # 登録時の処理
        dangerLocation = DangerLocations(
            latitude=float(request.GET.get('latitude')),
            longitude=float(request.GET.get('longitude')),
            dangerType=request.GET.get('danger_type')
        )

        dangerLocation.save()
    else:
        # 削除時の処理
        DangerLocations.objects.filter(
            latitude=float(request.GET.get('latitude')),
            longitude=float(request.GET.get('longitude')),
            dangerType=request.GET.get('danger_type')
        ).delete()

    return JsonResponse(response)
