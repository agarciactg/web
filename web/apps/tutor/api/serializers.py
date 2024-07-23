from rest_framework import serializers

from django.db.transaction import atomic

from web.apps.student.api.serializers import CandidateDetailSerializer
from web.apps.student.models import Candidate
from web.apps.tutor.models import Inscription, Tutor
from web.apps.users.api.serializers import UserDetailSummarySerializer
from web.apps.users.models import User


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

    # Data usuario - _t_three = tutor three
    first_name_t_three = serializers.CharField(write_only=True)
    last_name_t_three = serializers.CharField(write_only=True)
    email_t_three = serializers.CharField(write_only=True)
    type_document_t_three = serializers.IntegerField(write_only=True)
    document_number_t_three = serializers.IntegerField(write_only=True)
    avatar_t_three = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    username_t_three = serializers.CharField(write_only=True, required=True)
    avatar_url_t_three = serializers.URLField(
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
    email = serializers.CharField(write_only=True, max_length=350)

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
    vehicle_t_one = serializers.BooleanField(write_only=True, default=False)
    it_financial_t_one = serializers.BooleanField(write_only=True, default=False)

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
    vehicle_t_two = serializers.BooleanField(write_only=True, default=False)
    it_financial_t_two = serializers.BooleanField(write_only=True, default=False)

    # Data tutor 3
    phone_tutor_t_three = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    profession_t_three = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    workplace_t_three = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    phone_number_work_t_three = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    monthly_income_t_three = serializers.CharField(
        write_only=True, max_length=350, required=False, allow_null=True
    )
    type_of_housing_t_three = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
    vehicle_t_three = serializers.BooleanField(write_only=True, default=False)
    it_financial_t_three = serializers.BooleanField(write_only=True, default=False)

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
            user_candidate_data = {
                "username": validated_data.pop("username_c"),
                "type_user": 5,  # Es un estudiante, pero le falta validacion
                "first_name": validated_data.pop("first_name_c"),
                "last_name": validated_data.pop("last_name_c"),
                "type_document": validated_data.pop("type_document_c"),
                "document_number": validated_data.pop("document_number_c"),
                "email": validated_data.pop("email_c"),
                "avatar": validated_data.pop("avatar_c", None),
                "avatar_url": validated_data.pop("avatar_url_c", None),
            }

            user_tutor_one_data = {
                "username": validated_data.pop("username_t_one"),
                "type_user": 6,  # tipo de usuario Acudiente
                "first_name": validated_data.pop("first_name_t_one"),
                "last_name": validated_data.pop("last_name_t_one"),
                "type_document": validated_data.pop("type_document_t_one"),
                "document_number": validated_data.pop("document_number_t_one"),
                # "email": validated_data.pop("email_t_one"),
                "avatar": validated_data.pop("avatar_t_one", None),
                "avatar_url": validated_data.pop("avatar_url_t_one", None),
            }

            user_tutor_two_data = {
                "username": validated_data.pop("username_t_two"),
                "type_user": 6,  # tipo de usuario Acudiente
                "first_name": validated_data.pop("first_name_t_two"),
                "last_name": validated_data.pop("last_name_t_two"),
                "type_document": validated_data.pop("type_document_t_two"),
                "document_number": validated_data.pop("document_number_t_two"),
                "email": validated_data.pop("email_t_two"),
                "avatar": validated_data.pop("avatar_t_two", None),
                "avatar_url": validated_data.pop("avatar_url_t_two", None),
            }

            user_tutor_three_data = {
                "username": validated_data.pop("username_t_three"),
                "type_user": 6,  # tipo de usuario Acudiente
                "first_name": validated_data.pop("first_name_t_three"),
                "last_name": validated_data.pop("last_name_t_three"),
                "type_document": validated_data.pop("type_document_t_three"),
                "document_number": validated_data.pop("document_number_t_three"),
                "email": validated_data.pop("email_t_three"),
                "avatar": validated_data.pop("avatar_t_three", None),
                "avatar_url": validated_data.pop("avatar_url_t_three", None),
            }

            # informacion de candidato uno
            candidate_data = {
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
                # "phone": validated_data.pop("phone"),
                "email": validated_data.pop("email"),
            }

            # informacion de tutor uno
            tutor_one_data = {
                "phone": validated_data.pop("phone_tutor_t_one"),
                "profession": validated_data.pop("profession_t_one"),
                "email": validated_data.pop("email_t_one"),
                "workplace": validated_data.pop("workplace_t_one"),
                "phone_number_work": validated_data.pop("phone_number_work_t_one"),
                "monthly_income": validated_data.pop("monthly_income_t_one"),
                "type_of_housing": validated_data.pop("type_of_housing_t_one"),
                "vehicle": validated_data.pop("vehicle_t_one"),
                "it_financial": validated_data.pop("it_financial_t_one"),
            }

            # informacion de tutor dos
            tutor_two_data = {
                "phone": validated_data.pop("phone_tutor_t_two"),
                "profession": validated_data.pop("profession_t_two"),
                # "email": validated_data.pop("email_t_two"),
                "workplace": validated_data.pop("workplace_t_two"),
                "phone_number_work": validated_data.pop("phone_number_work_t_two"),
                "monthly_income": validated_data.pop("monthly_income_t_two"),
                "type_of_housing": validated_data.pop("type_of_housing_t_two"),
                "vehicle": validated_data.pop("vehicle_t_two"),
                "it_financial": validated_data.pop("it_financial_t_two"),
            }

            # informacion de tutor tres
            tutor_three_data = {
                "phone": validated_data.pop("phone_tutor_t_three"),
                "profession": validated_data.pop("profession_t_three"),
                # "email": validated_data.pop("email_t_three"),
                "workplace": validated_data.pop("workplace_t_three"),
                "phone_number_work": validated_data.pop("phone_number_work_t_three"),
                "monthly_income": validated_data.pop("monthly_income_t_three"),
                "type_of_housing": validated_data.pop("type_of_housing_t_three"),
                "vehicle": validated_data.pop("vehicle_t_three"),
                "it_financial": validated_data.pop("it_financial_t_three"),
            }

            inscription_data = {
                "civil_registration": validated_data.pop("civil_registration"),
                "vaccination_card": validated_data.pop("vaccination_card"),
                "identity_card": validated_data.pop("identity_card"),
                "last_newsletter": validated_data.pop("last_newsletter"),
                "work_record": validated_data.pop("work_record"),
                "photo_license": validated_data.pop("photo_license"),
                "registration_receipt": validated_data.pop("registration_receipt"),
            }

            # Save the information of the users
            user_candidate = User.objects.create(**user_candidate_data)
            user_candidate.save()

            # informacion tutors
            user_tutor_one = User.objects.create(**user_tutor_one_data)
            user_tutor_one.save()

            user_tutor_two = User.objects.create(**user_tutor_two_data)
            user_tutor_two.save()

            user_tutor_three = User.objects.create(**user_tutor_three_data)
            user_tutor_three.save()

            # creacion de candidato
            candidate = Candidate.objects.create(user=user_candidate, **candidate_data)
            candidate.save()

            # creacion de tutors
            tutor_one = Tutor.objects.create(user=user_tutor_one, **tutor_one_data)
            tutor_one.save()

            tutor_two = Tutor.objects.create(user=user_tutor_two, **tutor_two_data)
            tutor_two.save()

            tutor_three = Tutor.objects.create(user=user_tutor_three, **tutor_three_data)
            tutor_three.save()

            # creacion de inscripción
            inscription = Inscription.objects.create(candidate=candidate, **inscription_data)

            # agregar tutores a la inscripción
            inscription.tutors.add(tutor_one, tutor_two, tutor_three)
            inscription.save()

        return inscription


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
