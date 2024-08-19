from rest_framework import serializers

from django.db.transaction import atomic

from web.apps.student.api.serializers import CandidateDetailSerializer
from web.apps.student.models import Candidate
from web.apps.tutor.models import Inscription, Tutor
from web.apps.users.api.serializers import UserDetailSummarySerializer
from web.apps.users.models import User


def create_user(data, type_user):
    user_data = {
        "username": data.pop("username"),
        "type_user": type_user,
        "first_name": data.pop("first_name"),
        "last_name": data.pop("last_name"),
        "type_document": data.pop("type_document"),
        "document_number": data.pop("document_number"),
        "email": data.pop("email", None),  # Email opcional
        "avatar": data.pop("avatar", None),
        "avatar_url": data.pop("avatar_url", None),
    }
    user = User.objects.create(**user_data)
    user.save()
    return user


class InscriptionCreateSerializer(serializers.Serializer):
    """
    Serializer to create and update an inscription
    """

    # Data usuario - _c = candidato
    first_name_c = serializers.CharField(write_only=True)
    last_name_c = serializers.CharField(write_only=True)
    email_c = serializers.EmailField(write_only=True, max_length=250, required=True)
    type_document_c = serializers.IntegerField(write_only=True)
    document_number_c = serializers.IntegerField(write_only=True)
    avatar_c = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    username_c = serializers.CharField(write_only=True, required=True)
    avatar_url_c = serializers.URLField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )

    # Data usuario - _t_one = tutor one
    first_name_t_one = serializers.CharField(write_only=True)
    last_name_t_one = serializers.CharField(write_only=True)
    email_t_one = serializers.CharField(write_only=True)
    type_document_t_one = serializers.IntegerField(write_only=True)
    document_number_t_one = serializers.IntegerField(write_only=True)
    avatar_t_one = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    username_t_one = serializers.CharField(write_only=True, required=True)
    avatar_url_t_one = serializers.URLField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )

    # Data usuario - _t_two = tutor two
    first_name_t_two = serializers.CharField(write_only=True)
    last_name_t_two = serializers.CharField(write_only=True)
    email_t_two = serializers.CharField(write_only=True)
    type_document_t_two = serializers.IntegerField(write_only=True)
    document_number_t_two = serializers.IntegerField(write_only=True)
    avatar_t_two = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    username_t_two = serializers.CharField(write_only=True, required=True)
    avatar_url_t_two = serializers.URLField(
        write_only=True, allow_null=True, allow_blank=True, required=False
    )

    # Data candidate
    place_of_bird = serializers.CharField(write_only=True, max_length=350)
    date_of_bird = serializers.DateField(write_only=True)
    years = serializers.IntegerField(write_only=True)
    gender = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    laterality = serializers.IntegerField(write_only=True)
    degrees = serializers.IntegerField(write_only=True)
    elective_year = serializers.IntegerField(write_only=True)
    address = serializers.CharField(write_only=True, max_length=350)
    city = serializers.CharField(write_only=True, max_length=350)
    neighborhood = serializers.CharField(write_only=True, max_length=350)
    stratum = serializers.IntegerField(write_only=True)
    phone = serializers.CharField(write_only=True, max_length=350, required=False, allow_null=True)
    # email = serializers.CharField(write_only=True, max_length=350, required=False, allow_null=True)

    # Data tutor 1
    phone_tutor_t_one = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    profession_t_one = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    workplace_t_one = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    phone_number_work_t_one = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    monthly_income_t_one = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    type_of_housing_t_one = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
    vehicle_t_one = serializers.BooleanField(write_only=True, default=False, required=False, allow_null=True)
    it_financial_t_one = serializers.BooleanField(write_only=True, default=False, required=False, allow_null=True)

    # Data tutor 2
    phone_tutor_t_two = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    profession_t_two = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    workplace_t_two = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    phone_number_work_t_two = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    monthly_income_t_two = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    type_of_housing_t_two = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
    vehicle_t_two = serializers.BooleanField(write_only=True, default=False, required=False, allow_null=True)
    it_financial_t_two = serializers.BooleanField(write_only=True, default=False, required=False, allow_null=True)

    # Data inscription
    civil_registration = serializers.FileField(write_only=True, required=False, allow_null=True)
    vaccination_card = serializers.FileField(write_only=True)
    identity_card = serializers.FileField(write_only=True)
    last_newsletter = serializers.FileField(write_only=True)
    work_record = serializers.FileField(write_only=True)
    photo_license = serializers.ImageField(write_only=True, required=False, allow_null=True)
    registration_receipt = serializers.ImageField(write_only=True)

    def create(self, validated_data):
        with atomic():
            # Crear usuario candidato
            user_candidate = self.create_user(validated_data, "_c")
            candidate = Candidate.objects.create(user=user_candidate, **self.extract_candidate_data(validated_data))
            candidate.save()

            # Crear tutores
            tutors = []
            for tutor_key in ["_t_one", "_t_two"]:
                user_tutor = self.create_user(validated_data, tutor_key)
                tutor_data = self.extract_tutor_data(validated_data, tutor_key)
                tutor = Tutor.objects.create(user=user_tutor, **tutor_data)
                tutor.save()
                tutors.append(tutor)

            # Crear inscripción
            inscription_data = self.extract_inscription_data(validated_data)
            inscription = Inscription.objects.create(candidate=candidate, **inscription_data)
            inscription.tutors.add(*tutors)
            inscription.save()

        return inscription

    def create_user(self, validated_data, suffix):
        user_data = {
            "username": validated_data.pop(f"username{suffix}"),
            "type_user": 5,  # tipo de usuario Estudiante
            "first_name": validated_data.pop(f"first_name{suffix}"),
            "last_name": validated_data.pop(f"last_name{suffix}"),
            "type_document": validated_data.pop(f"type_document{suffix}"),
            "document_number": validated_data.pop(f"document_number{suffix}"),
            "email": validated_data.pop(f"email{suffix}", None),  # Email opcional
            "avatar": validated_data.pop(f"avatar{suffix}", None),
            "avatar_url": validated_data.pop(f"avatar_url{suffix}", None),
        }
        return User.objects.create(**user_data)

    def extract_tutor_data(self, validated_data, suffix):
        return {
            "phone": validated_data.pop(f"phone_tutor{suffix}"),
            "profession": validated_data.pop(f"profession{suffix}"),
            "workplace": validated_data.pop(f"workplace{suffix}"),
            "phone_number_work": validated_data.pop(f"phone_number_work{suffix}"),
            "monthly_income": validated_data.pop(f"monthly_income{suffix}"),
            "type_of_housing": validated_data.pop(f"type_of_housing{suffix}"),
            "vehicle": validated_data.pop(f"vehicle{suffix}"),
            "it_financial": validated_data.pop(f"it_financial{suffix}"),
        }

    def extract_candidate_data(self, validated_data):
        return {
            "place_of_bird": validated_data.pop("place_of_bird"),
            "date_of_bird": validated_data.pop("date_of_bird"),
            "years": validated_data.pop("years"),
            "gender": validated_data.pop("gender"),
            "laterality": validated_data.pop("laterality"),
            "degrees": validated_data.pop("degrees"),
            "elective_year": validated_data.pop("elective_year"),
            "address": validated_data.pop("address"),
            "city": validated_data.pop("city"),
            "neighborhood": validated_data.pop("neighborhood"),
            "stratum": validated_data.pop("stratum"),
            # "email": validated_data.pop("email"),
        }

    def extract_inscription_data(self, validated_data):
        return {
            "civil_registration": validated_data.pop("civil_registration"),
            "vaccination_card": validated_data.pop("vaccination_card"),
            "identity_card": validated_data.pop("identity_card"),
            "last_newsletter": validated_data.pop("last_newsletter"),
            "work_record": validated_data.pop("work_record"),
            "photo_license": validated_data.pop("photo_license"),
            "registration_receipt": validated_data.pop("registration_receipt"),
        }


class TutorDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSummarySerializer(many=False)

    class Meta:
        model = Inscription
        fields = (
            "id",
            "uuid",
            "user",
            "phone",
            "profession",
            "monthly_income",
            "email",
            "workplace",
            "type_of_housing",
            "vehicle",
            "it_financial",
        )


class InscriptionDetailSerializer(serializers.ModelSerializer):

    candidate = CandidateDetailSerializer(many=False)
    tutors = TutorDetailSerializer(many=True)

    class Meta:
        model = Inscription
        fields = (
            "id",
            "uuid",
            "candidate",
            "tutors",
            "civil_registration",
            "vaccination_card",
            "identity_card",
            "last_newsletter",
            "work_record",
            "photo_license",
            "registration_receipt",
        )
