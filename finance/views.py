import uuid, json, traceback
from django.http import JsonResponse
from rest_framework.views import APIView
from finance.models import FinancialAdvisor, ALLOWED_FIELDS
from finance.finance_ai_service import FinanceAIService


class FinancialAdvisorView(APIView):

    def get(self, request, conv_id=None):
        if not conv_id:
            return JsonResponse({"error": "id is required"}, status=400)

        try:
            record = FinancialAdvisor.objects.get(id=conv_id)
        except FinancialAdvisor.DoesNotExist:
            print(traceback.print_exc())
            return JsonResponse({"error": "Record not found"}, status=404)

        return JsonResponse(record.show(), status=200)

    def post(self, request, conv_id=None):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            print(traceback.print_exc())
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        fields = {k: v for k, v in body.items() if k in ALLOWED_FIELDS}

        # UPDATE
        if conv_id:
            try:
                record = FinancialAdvisor.objects.get(id=conv_id)
            except FinancialAdvisor.DoesNotExist:
                print(traceback.print_exc())
                return JsonResponse({"error": "Record not found"}, status=404)

            for field, value in fields.items():
                setattr(record, field, value)
            record.save()

            return JsonResponse(record.show(), status=200)

        # CREATE
        else:
            record = FinancialAdvisor.objects.create(**fields)
            return JsonResponse(record.show(), status=201)

class FinancialAdvisorReportGenerator(APIView):

    def post(self, request, conv_id):
        try:
            record = FinancialAdvisor.objects.get(id=conv_id)
        except FinancialAdvisor.DoesNotExist:
            print(traceback.print_exc())
            return JsonResponse({"error": "Record not found"}, status=404)

        try:
            service = FinanceAIService()
            record = service.generate(record)
        except ValueError as e:
            print(traceback.print_exc())
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(record.show(), status=200)
