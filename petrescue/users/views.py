# In users/views.py

from rest_framework import viewsets, permissions, status , generics 
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from pets.models import Pet, PetReport
from pets.serializers import PetSerializer


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Return the authenticated user's data.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- THIS METHOD IS NOW CORRECTED ---
    @action(detail=True, methods=['get']) # Change detail=False to detail=True
    def pets(self, request, pk=None):
        """
        Return a list of pets reported by the user.
        """
        if pk == 'me':
            user = request.user
        else:
            # This allows an admin to see pets for a specific user ID
            user = self.get_object()
        
        reports = PetReport.objects.filter(user=user)

        tab = request.query_params.get('tab', None)
        if tab:
            if tab == 'lost':
                reports = reports.filter(pet_status='Lost')
            elif tab == 'found':
                reports = reports.filter(pet_status='Found')
            elif tab == 'adopt':
                reports = reports.filter(pet_status='Adopted')
        
        pet_ids = reports.values_list('pet_id', flat=True)
        pets = Pet.objects.filter(id__in=pet_ids)
        
        serializer = PetSerializer(pets, many=True, context={'request': request})
        return Response(serializer.data)
    # --- END OF CORRECTION ---

        # --- NEW METHOD ADDED HERE ---
    def perform_destroy(self, instance):
        """
        Perform a soft delete by setting the user's is_active flag to False.
        """
        instance.is_active = False
        instance.save()
    # --- END OF NEW METHOD ---

    def get_permissions(self):
        """
        Assigns permissions based on the action.
        """
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action in ['me', 'pets']:
             self.permission_classes = [permissions.IsAuthenticated]
        else: # This applies to 'retrieve', 'update', 'partial_update', 'destroy'
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        return super().get_permissions()

# --- ADD THIS NEW VIEW AT THE BOTTOM ---

class PasswordResetRequestView(generics.GenericAPIView):
    """
    View for initiating a password reset request.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # This line will now work because it's imported
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"http://localhost:3000/reset-password/{uidb64}/{token}/"
            print("--- PASSWORD RESET LINK (for development) ---")
            print(reset_link)
            print("---------------------------------------------")

        except User.DoesNotExist:
            pass
        
        return Response(
            {"detail": "If an account with this email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )
    

# --- ADD THIS NEW VIEW AT THE BOTTOM ---
class PasswordResetConfirmView(generics.GenericAPIView):
    """
    View for confirming the password reset.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        uidb64 = validated_data['uidb64']
        token = validated_data['token']
        password = validated_data['password']

        try:
            # This line will now work because smart_str is imported
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)
