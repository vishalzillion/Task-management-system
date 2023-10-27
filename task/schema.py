
import graphene
from graphene_django.types import DjangoObjectType
from graphene import relay
import graphql_jwt
from django.contrib.auth import authenticate,get_user_model
from .models import Task,Category
from graphql_jwt.decorators import login_required
from graphene_django.fields import DjangoConnectionField
from django.db.models import Q


from graphql_jwt.shortcuts import get_token,create_refresh_token

User=get_user_model()




class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )

class TaskType(DjangoObjectType):
    class Meta:
        model = Task    
        interfaces = (relay.Node, )    

class CategoryType(DjangoObjectType):
   class Meta:
       model = Category

import graphene

class WeeklyTaskStatsType(graphene.ObjectType):
    total_assigned_tasks = graphene.Int()
    total_pending_tasks = graphene.Int()
    total_completed_tasks = graphene.Int()
          

class CreateCategory(graphene.Mutation):
   class Arguments:
       name = graphene.String(required=True)




   category = graphene.Field(CategoryType)

   @classmethod
   @login_required
   def mutate(cls, root, info, name):
       if not info.context.user.is_superuser:
           raise Exception('Must be a superuser to create categories')

       category = Category(name=name)
       category.save()

       return CreateCategory(category=category)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    
    token = graphene.String()
    refresh_token = graphene.String()
    
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

      
        token = get_token(user)
        
        
        return CreateUser(user=user,token=token)
    



class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        priority = graphene.String()
        category_id = graphene.Int()
        username = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, title, description ,priority, category_id,username):
        user = info.context.user

        if user.is_superuser:
            # Get the Category object based on the provided category_id
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise Exception("Category with the provided ID does not exist.")
            try:
                uname = User.objects.get(username=username)
            except:
                raise Exception("User with this username does not exist")    
            # Create the task
            task = Task(
                title=title,
                description=description,
                priority=priority,
                category=category,
                assigned_to=uname  
            )
            task.save()
            return CreateTask(task=task)
        else:
            raise Exception("Only superusers can create tasks.")

class MarkTaskCompleted(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)

    task = graphene.Field(TaskType)

    @classmethod
    @login_required
    def mutate(cls, root, info, task_id):
        user = info.context.user
        task = Task.objects.get(pk=task_id)

        # Check task is assigned to user
        if task.assigned_to != user:
            raise Exception('Permission denied')
        
        task.status = Task.COMPLETED
        task.save()

        return MarkTaskCompleted(task=task)
   
# schema.py
      

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    create_task = CreateTask.Field()

    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    mark_task_completed = MarkTaskCompleted.Field()
    create_category = CreateCategory.Field()



class Query(graphene.ObjectType):
    

    all_tasks = graphene.List(TaskType, 
        first=graphene.Int(), 
        last=graphene.Int(),
        due_date=graphene.String(),
        priority=graphene.String(),
        category_id=graphene.Int())

    search_tasks = graphene.List(TaskType, search=graphene.String())
    weekly_stats = graphene.Field(WeeklyTaskStatsType,start=graphene.Date(),end=graphene.Date())

    
    def resolve_weekly_stats(self, info, start, end):
        # Filter tasks created within the specified date range
        tasks_within_date_range = Task.objects.filter(created_at__range=(start, end))

        # Count the total tasks within the date range
        total_tasks = tasks_within_date_range.count()

        # Filter and count pending tasks within the date range
        total_pending_task = tasks_within_date_range.filter(status=Task.PENDING).count()

        # Filter and count completed tasks within the date range
        total_completed_task = tasks_within_date_range.filter(status=Task.COMPLETED).count()

        # You can return these statistics in a custom type, e.g., WeeklyStatsType
        return WeeklyTaskStatsType(
            total_assigned_tasks=total_tasks,
            total_pending_tasks=total_pending_task,
            total_completed_tasks=total_completed_task
        )



    
        

    @login_required
    def resolve_all_tasks(self, info, first=None, last=None, due_date=None, priority=None, category_id=None):
        if info.context.user.is_superuser:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(assigned_to=info.context.user)    
        
        # Apply filters
        if due_date:
            # Assuming due_date is a string in ISO format (e.g., '2023-10-31')
            queryset = queryset.filter(due_date=due_date)
        
        if priority:
            queryset = queryset.filter(priority=priority)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Apply sorting
        queryset = queryset.order_by('due_date')  # Sort by due date in ascending order

        if first is not None:
            queryset = queryset[:first]
        elif last is not None:
            queryset = queryset.order_by('-id')[:last]

        return queryset

      
    @login_required
    def resolve_search_tasks(self, info, search):
        if info.context.user.is_superuser:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(assigned_to=info.context.user)

        if search:
            # Use the Q object to perform a case-insensitive search on title and description fields
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return queryset
    

  
schema = graphene.Schema(query=Query, mutation=Mutation)    



