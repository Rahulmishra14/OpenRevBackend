from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from accounts.serializer import UserProfileSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    full_name = request.data.get('fullname')

    if not email or not password or not full_name:
        return Response({'error': 'Email, full name, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return Response({'error': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if email is already in use
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a username from the email (you can customize this logic)
    base_username = email.split('@')[0]
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)

    # Set full name
    names = full_name.strip().split(' ', 1)
    user.first_name = names[0]
    if len(names) > 1:
        user.last_name = names[1]
    user.save()

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(request, username=user_obj.username, password=password)

    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return Response({'message': 'Login successful', 'user': user_data, 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_api(request):
    print("Session ID received:", request.COOKIES.get('sessionid'))
    user = request.user
    return Response({
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": f"{user.first_name} {user.last_name}".strip(),
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def profile_list_api(request):
    email = request.GET.get('email')
    user_id = request.GET.get('id')

    queryset = User.objects.all()
    if email:
        queryset = queryset.filter(email=email)
    if user_id:
        queryset = queryset.filter(id=user_id)

    serializer = UserProfileSerializer(queryset, many=True)
    return Response({'profiles': serializer.data}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def profile_detail_api(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def open_submissions_api(request):
    data = {
        "submissions": [
            {
                "id": "ICML2025_AI4MATH",
                "title": "ICML 2025 Workshop AI4MATH",
                "deadline": "2025-06-21T23:59:00Z"
            },
            {
                "id": "GSCL2025_CPSS",
                "title": "GSCL KONVENS 2025 Workshop CPSS",
                "deadline": "2025-06-22T07:00:00Z"
            },
            {
                "id": "ICCV2025_SEA",
                "title": "ICCV 2025 Workshop SEA",
                "deadline": "2025-06-23T05:00:00Z"
            }
        ]
    }
    return Response(data)



ACTIVE_VENUES = {
    "groups": [
        {
            "id": "active_venues",
            "cdate": 1595932124826,
            "ddate": None,
            "tcdate": None,
            "tmdate": 1750450706275,
            "tddate": None,
            "web": None,
            "signatures": ["OpenReview.net/Support"],
            "signatories": ["OpenReview.net"],
            "readers": ["everyone"],
            "nonreaders": [],
            "writers": ["OpenReview.net/Support"],
            "members": [
                "TMLR",
                "Computo",
                "DMLR",
                "YouthLACIGF.lat/2024/Edition",
                "ISAPh/2024/Symposium",
                "MSLD/2024/Meeting",
                "icaps-conference.org/ICAPS/2024/Demo_Track",
                "sfb1102.uni-saarland.de/RAILS/2025/Conference",
                "jpmorganchase.com/2025/ML/Conference"
            ]
        }
    ]
}

HOST_GROUP = {
    "groups": [
        {
            "id": "host",
            "cdate": 1495570582864,
            "ddate": None,
            "tcdate": None,
            "tmdate": 1750269735058,
            "tddate": None,
            "tauthor": "OpenReview.net",
            "web": None,
            "signatures": ["~Super_User1"],
            "signatories": ["OpenReview.net"],
            "readers": ["everyone"],
            "nonreaders": [],
            "writers": ["OpenReview.net"],
            "members": [
                "ICLR.cc",
                "auai.org/UAI",
                "ICML.cc",
                "ACM.org",
                "AKBC.ws",
                "learningtheory.org/COLT",
                "eswc-conferences.org/ESWC",
                "IEEE.org",
                "ISMIR.net",
                "swsa.semanticweb.org/ISWC",
                "machineintelligence.cc/MIC",
                "MIDL.io",
                "roboticsfoundation.org/RSS"
            ]
        }
    ]
}

INVITATIONS = {
    "invitations": [
        {
            "reply": {
                "readers": {
                    "values-copied": [
                        "microsoft.com/AI4Science/2022/Internal/PBS",
                        "{content.authorids}",
                        "{signatures}"
                    ]
                },
                "writers": {
                    "values-copied": [
                        "microsoft.com/AI4Science/2022/Internal/PBS",
                        "{content.authorids}",
                        "{signatures}"
                    ]
                },
                "signatures": {
                    "values-regex": "~.*"
                },
                "content": {
                    "title": {
                        "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                        "order": 1,
                        "value-regex": "(?!^ +$)^.{1,250}$",
                        "required": True
                    },
                    "authors": {
                        "description": "List of author names",
                        "order": 2,
                        "values-regex": "^.{1,5000}$",
                        "required": True
                    }
                }
            }
        }
    ]
}

WEBFIELD = """// Webfield component
return {
  component: 'VenueHomepage',
  properties: {
    header: {
      title: '2nd AI for Math Workshop @ ICML 2025',
      subtitle: 'AI4MATH',
      website: 'https://sites.google.com/view/ai4mathworkshopicml2025',
      contact: 'ai4mathicml@gmail.com',
      location: 'Vienna, Austria',
      instructions: 'Please see the venue website for more information.',
      date: 'Jul 18 2025',
      deadline: 'Submission Start: Mar 18 2025 11:59PM UTC-0, Submission Deadline: Jun 21 2025 11:59AM UTC-0'
    },
     submission_id: 'ICML.cc/2025/Workshop/AI4MATH/-/Submission',
    parentGroupId: 'ICML.cc/2025/Workshop',
    "submission_id": "ICML.cc/2025/Workshop/AI4MATH/-/Submission",
    "tabs": [
        {"name": "Recent Activity", "type": "activity"}
    ],


  }
}"""


@api_view(['GET'])
def notes_edits(request):
    domain = request.GET.get('domain')
    if domain == 'ICML.cc/2025/Workshop/AI4MATH':
        return Response({
            "notes": [
                {
                    "id": "AI4MATH-paper1",
                    "invitation": "ICML.cc/2025/Workshop/AI4MATH/-/Submission",
                    "signatures": ["ICML.cc/2025/Workshop/AI4MATH/Authors"],
                    "readers": ["everyone"],
                    "writers": ["ICML.cc/2025/Workshop/AI4MATH/Authors"],
                    "content": {
                        "title": "An Amazing Math AI Paper",
                        "abstract": "This paper explores mathematical reasoning in AI.",
                        "authors": ["Alice", "Bob"],
                        "authorids": ["~Alice1", "~Bob1"]
                    }
                }
            ]
        })
    else:
        return Response({"notes": []})

@api_view(['GET'])
def groups_api(request):
    group_id = request.GET.get('id')
    if group_id == 'active_venues':
        return Response(ACTIVE_VENUES)
    elif group_id == 'host':
        return Response(HOST_GROUP)
    elif group_id == 'ICML.cc/2025/Workshop/AI4MATH':
        return Response({
        "groups": [{
            "id": group_id,
            "signatures": ["~Super_User1"],
            "signatories": [group_id],
            "readers": ["everyone"],
            "writers": [group_id],
            "invitations": [
                "OpenReview.net/-/Edit",
                f"{group_id}/-/Edit"
            ],
            "domain": group_id,
            "parent": "ICML.cc/2025/Workshop",
            "details": {
                "writable": True
            },
            "content": {
                "title": {"value": "2nd AI for Math Workshop @ ICML 2025"},
                "subtitle": {"value": "AI4MATH"},
                "website": {"value": "https://sites.google.com/view/ai4mathworkshopicml2025"},
                "contact": {"value": "ai4mathicml@gmail.com"},
                "location": {"value": "Vienna, Austria"},
                "instructions": {"value": "Please see the venue website for more information."},
                "date": {"value": "Jul 18 2025"},
                "deadline": {"value": "Submission Start: Mar 18 2025 11:59PM UTC-0, Submission Deadline: Jun 21 2025 11:59AM UTC-0"},
                "submission_id": {"value": f"{group_id}/-/Submission"},
                "parentGroupId": {"value": "ICML.cc/2025/Workshop"},
                "meta_invitation_id": {"value": f"{group_id}/-/Edit"},
                "submission_name": {"value": "Submission"},
                "submission_venue_id": {"value": f"{group_id}/Submission"},
                "withdrawn_venue_id": {"value": f"{group_id}/Withdrawn_Submission"},
                "desk_rejected_venue_id": {"value": f"{group_id}/Desk_Rejected_Submission"},
                "rejected_venue_id": {"value": f"{group_id}/Rejected_Submission"},
                "public_submissions": {"value": False},
                "submission_email_template": {
                    "value": "Your submission to AI4MATH has been {{action}}.\n\nSubmission Number: {{note_number}} \n\nTitle: {{note_title}} \n\nTo view your submission, click here: https://openreview.net/forum?id={{note_forum}}"
                },
                "submission_email_pcs": {"value": False},
                "program_chairs_id": {"value": f"{group_id}/Program_Chairs"},
                "reviewers_id": {"value": f"{group_id}/Reviewers"},
                "authors_id": {"value": f"{group_id}/Authors"},
                "authors_name": {"value": "Authors"},
                "withdraw_expiration_id": {"value": f"{group_id}/-/Withdraw_Expiration"},
                "desk_reject_expiration_id": {"value": f"{group_id}/-/Desk_Reject_Expiration"},
                "automatic_reviewer_assignment": {"value": True},
                "review_name": {"value": "Official_Review"},
                "review_email_pcs": {"value": False},
                "comment_mandatory_readers": {"value": [f"{group_id}/Program_Chairs"]},
                "comment_email_pcs": {"value": False},
                "rebuttal_name": {"value": "Rebuttal"},
                "reviewer_roles": {"value": ["Reviewers"]}
            },
            "submission_id": "ICML.cc/2025/Workshop/AI4MATH/-/Submission",
            "tabs": [
                {"name": "Recent Activity", "type": "activity"}
            ],


            "web": WEBFIELD
        }]
    }, status=status.HTTP_200_OK)


    else:
        return Response({"groups": []})

@api_view(['GET'])
def invitations_api(request):
    invitee = request.GET.get('invitee')
    pastdue = request.GET.get('pastdue') == 'false'
    invitation_type = request.GET.get('type')
    invitation_id = request.GET.get('id')

    future_due = 1760000000000

    # 🎯 SINGLE INVITATION BY ID
    if invitation_id == 'ICML.cc/2025/Workshop/AI4MATH/-/Submission':
        return Response({
            "invitations": [
                {
                    "id": invitation_id,
                    "signatures": ["ICML.cc/2025/Workshop/AI4MATH"],
                    "readers": ["everyone"],
                    "writers": ["ICML.cc/2025/Workshop/AI4MATH"],
                    "invitees": ["everyone"],
                    "multiReply": False,
                    "duedate": future_due,
                    "details": {
                        "writable": True
                    },
                    "reply": {
                        "readers": {"values": ["everyone"]},
                        "writers": {"values-copied": ["authors"]},
                        "signatures": {"values-regex": "~.*"},
                        "content": {
                            "title": {"order": 1, "value": "string"},
                            "abstract": {"order": 2, "value": "string"},
                            "authors": {"order": 3, "value": ["string"]}
                        }
                    }
                }
            ]
        })

    # 🎯 LIST ALL ACTIVE
    if invitee == '~' and pastdue and invitation_type == 'all':
        return Response({
            "invitations": [
                {
                    "id": "ICML.cc/2025/Workshop/AI4MATH/-/Submission",
                    "duedate": future_due,
                    "details": {"writable": True},
                    "reply": {
                        "readers": {"values": ["everyone"]},
                        "writers": {"values-copied": ["authors"]},
                        "signatures": {"values-regex": "~.*"},
                        "content": {
                            "title": {"order": 1, "value": "string"},
                            "abstract": {"order": 2, "value": "string"},
                            "authors": {"order": 3, "value": ["string"]}
                        }
                    }
                },
                {
                    "id": "GSCL.cc/2025/Workshop/CPSS/-/Submission",
                    "duedate": 1750200000000,
                    "details": {"writable": True}
                },
                {
                    "id": "IEEE.org/ISWC/2025/-/Submission",
                    "duedate": 1750400000000,
                    "details": {"writable": True}
                }
            ]
        })

    return Response({"invitations": []})





# @api_view(['GET'])
# def group_detail_api(request):
#     group_id = request.GET.get('id')
#     if not group_id:
#         return Response({'error': 'Group id is required'}, status=400)
    
#     if group_id == "ICML.cc/2025/Workshop/AI4MATH":
#         return Response({
#             "groups": [{
#                 "id": group_id,
#                 "title": "2nd AI for Math Workshop @ ICML 2025",
#                 "web": "https://sites.google.com/view/ai4mathworkshopicml2025",
#                 "contact": "ai4mathicml@gmail.com",
#                 "short_name": "AI4Math@ICML25",
#                 "start_date": "2025-07-18",
#                 "description": "Please see the venue website for more information.",
#                 "members": [],  # if you track chairs/editors
#             }]
#         }, status=status.HTTP_200_OK)

#     # Dummy metadata
#     group_info = {
#         'id': group_id,
#         'title': group_id.split('/')[-1].replace('_', ' '),
#         'description': f'Dummy description for {group_id}.',
#         'editors': ['editor1@example.com', 'editor2@example.com'],
#     }

#     # Dummy invitations
#     invitations = [
#         {
#             'id': f'{group_id}/-/Submission',
#             'duedate': 1750500000000,
#             'content': {'due_date': '2025-07-01T23:59:00Z'}
#         },
#         {
#             'id': f'{group_id}/-/Withdraw',
#             'duedate': 1750600000000,
#             'content': {'due_date': '2025-07-02T23:59:00Z'}
#         }
#     ]

#     return Response({'group': group_info, 'invitations': invitations})