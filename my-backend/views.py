from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from models import User, Resource

COURSES_DATA_BY_LEVEL = {
    '1-1': {
        'courses': [
            {'id': 1, 'name': 'EEE 181', 'title': 'Basic Electrical Engineering'},
            {'id': 2, 'name': 'MATH 181', 'title': 'Differential and Integral Calculus'},
            {'id': 3, 'name': 'MATH 183', 'title': 'Ordinary & Partial Differential Equations and Matrix'},
            {'id': 4, 'name': 'CHEM 181', 'title': 'Chemistry'},
            {'id': 5, 'name': 'HUM 181', 'title': 'Technical English'},
        ],
        'labs': [
            {'id': 1, 'name': 'EEE 182', 'title': 'Basic Electrical Engineering Sessional'},
            {'id': 2, 'name': 'CHEM 182', 'title': 'Chemistry Sessional'},
            {'id': 3, 'name': 'ME 182', 'title': 'Mechanical Engineering Drawing'},
        ]
    },
    # Add more levels as needed...
}

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        email = data.get('email')
        password = data.get('password')
        
        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({'success': False, 'message': 'User with this ID already exists'})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'User with this email already exists'})
        
        user = User.objects.create_user(
            username=user_id,
            user_id=user_id,
            email=email,
            password=password,
            first_name=data.get('name', ''),
            phone=data.get('phone', ''),
            batch=data.get('batch', ''),
            address=data.get('address', ''),
            role='student'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Student registration successful! Wait for admin approval.',
            'user': {
                'id': user.user_id,
                'name': user.first_name,
                'email': user.email,
                'batch': user.batch,
                'role': 'student'
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        password = data.get('password')
        
        try:
            user = User.objects.get(user_id=user_id)
            if not user.check_password(password):
                return JsonResponse({'success': False, 'message': 'Invalid ID or password'}, status=401)
            
            return JsonResponse({
                'success': True,
                'message': 'Login successful!',
                'user': {
                    'id': user.user_id,
                    'name': user.first_name,
                    'email': user.email,
                    'batch': user.batch,
                    'role': user.role
                }
            })
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid ID or password'}, status=401)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def health(request):
    users_count = User.objects.count()
    resources_count = Resource.objects.count()
    return JsonResponse({
        'status': 'ok',
        'message': 'ETE Resource Portal API is running',
        'usersCount': users_count,
        'resourcesCount': resources_count
    })


@csrf_exempt
@require_http_methods(["GET"])
def materials(request, resource_type, level, term):
    try:
        level_term_key = f"{level}-{term}"
        course_data = COURSES_DATA_BY_LEVEL.get(level_term_key, {}).get('courses', [])
        lab_data = COURSES_DATA_BY_LEVEL.get(level_term_key, {}).get('labs', [])
        
        # Get approved uploads
        approved_uploads = Resource.objects.filter(
            level=str(level),
            term=str(term),
            status='approved'
        )
        
        if resource_type == 'labs':
            filtered_uploads = approved_uploads.filter(resource_type='Lab')
            data = lab_data
        else:
            filtered_uploads = approved_uploads.exclude(resource_type='Lab')
            data = course_data
        
        merged_data = list(data)
        
        for upload in filtered_uploads:
            existing = next((d for d in merged_data if d.get('name') == upload.course_code), None)
            if not existing:
                merged_data.append({
                    'id': len(merged_data) + 1,
                    'name': upload.course_code,
                    'title': upload.course_name,
                    'isUserUpload': True,
                    'fileTitle': upload.file_title,
                    'description': upload.description,
                    'uploadedBy': upload.user_name,
                    'filename': upload.file.name if upload.file else None
                })
        
        return JsonResponse({
            'success': True,
            'type': resource_type,
            'level': level,
            'term': term,
            'data': merged_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def upload_resource(request):
    try:
        user_id = request.POST.get('userId')
        user_name = request.POST.get('userName')
        batch = request.POST.get('batch')
        level = request.POST.get('level')
        term = request.POST.get('term')
        course_code = request.POST.get('courseCode')
        course_name = request.POST.get('courseName')
        resource_type = request.POST.get('resourceType')
        file_title = request.POST.get('fileTitle')
        description = request.POST.get('description')
        
        user = None
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            pass
        
        file_obj = request.FILES.get('file', None)
        
        resource = Resource.objects.create(
            user=user,
            user_name=user_name,
            batch=batch,
            level=level,
            term=term,
            course_code=course_code,
            course_name=course_name,
            resource_type=resource_type,
            file_title=file_title,
            description=description,
            file=file_obj,
            status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'File uploaded successfully! It will be reviewed soon.' if file_obj else 'Resource metadata saved! It will be reviewed soon.',
            'resource': {
                'id': resource.id,
                'userId': user_id,
                'userName': user_name,
                'status': 'pending'
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def user_uploads(request, user_id):
    try:
        user_resources = Resource.objects.filter(user__user_id=user_id).order_by('-uploaded_at')
        data = [{
            'id': r.id,
            'fileTitle': r.file_title,
            'courseName': r.course_name,
            'courseCode': r.course_code,
            'status': r.status,
            'uploadedAt': r.uploaded_at.isoformat(),
            'file': {'filename': r.file.name if r.file else None} if r.file else None,
            'reviewComment': r.review_comment
        } for r in user_resources]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def admin_all_resources(request):
    try:
        resources = Resource.objects.all().order_by('-uploaded_at')
        data = [{
            'id': r.id,
            'fileTitle': r.file_title,
            'courseName': r.course_name,
            'courseCode': r.course_code,
            'userName': r.user_name,
            'status': r.status,
            'uploadedAt': r.uploaded_at.isoformat(),
            'file': {'filename': r.file.name if r.file else None} if r.file else None,
            'reviewComment': r.review_comment
        } for r in resources]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def review_resource(request):
    try:
        data = json.loads(request.body)
        resource_id = data.get('resourceId')
        status = data.get('status')
        review_comment = data.get('reviewComment', '')
        admin_id = data.get('adminId', 'admin')
        
        if status not in ['approved', 'rejected']:
            return JsonResponse({'success': False, 'message': 'Invalid status'}, status=400)
        
        resource = Resource.objects.get(id=resource_id)
        resource.status = status
        resource.review_comment = review_comment
        resource.reviewed_at = datetime.now()
        resource.admin_id = admin_id
        resource.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Resource {status} successfully',
            'resource': {
                'id': resource.id,
                'status': resource.status
            }
        })
    except Resource.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Resource not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_resource(request, resource_id):
    try:
        resource = Resource.objects.get(id=resource_id)
        if resource.file:
            resource.file.delete()
        resource.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Resource deleted successfully'
        })
    except Resource.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Resource not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
