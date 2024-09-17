#solve drf-swagger bug      done
#install pillow      done
#uncomment logo in organisation   done

path(
        "get-user-average-stats-by-range/<int:user_id>/year/<int:year>/start-month/<str:start_month>/end-month/<str:end_month>/",
        views.GetUserVoiceInsightsStatisticsByRangeView.as_view(),
    ),
    path(
        "get-user-total-stats-by-range/<int:user_id>/year/<int:year>/start-month/<str:start_month>/end-month/<str:end_month>/",
        views.GetUserVoiceInsightsTotalStatisticsByRangeView.as_view(),
    ),
class GetUserVoiceInsightsStatisticsByRangeView(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, user_id, year, start_month, end_month, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        voice_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
            month__gte=start_month,
            month__lte=end_month,
        )

        if not voice_insights.exists():
            return Response(
                {"message": "No voice insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = voice_insights.first().managed_by
        grade_counts = voice_insights.values("grade").annotate(count=Count("grade"))

        all_voice_insights_stats = {
            "Year": year,
            "start_month": start_month,
            "end_month": end_month,
            "managed_by": managed_by,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "average_stats": {
                "average_aes": round(
                    voice_insights.values("aes").aggregate(Avg("aes"))["aes__avg"], 2
                ),
                "average_outbound": round(
                    voice_insights.values("actual_outbound_calls").aggregate(
                        Avg("actual_outbound_calls")
                    )["actual_outbound_calls__avg"],
                    2,
                ),
                "average_talktime": round(
                    voice_insights.values("actual_talktime").aggregate(
                        Avg("actual_talktime")
                    )["actual_talktime__avg"],
                    2,
                ),
                "average_inbound_calls": round(
                    voice_insights.values("actual_inbound_calls").aggregate(
                        Avg("actual_inbound_calls")
                    )["actual_inbound_calls__avg"],
                    2,
                ),
                "average_csat": round(
                    voice_insights.values("csat").aggregate(Avg("csat"))["csat__avg"], 2
                ),
                "average_overall_score": round(
                    voice_insights.values("overall_score").aggregate(
                        Avg("overall_score")
                    )["overall_score__avg"],
                    2,
                ),
            },
        }

        return Response(all_voice_insights_stats, status=status.HTTP_200_OK)
    
class GetUserVoiceInsightsTotalStatisticsByRangeView(GenericAPIView):
    permission_classes = []
    serializer_class = VoiceInsightsRetrieveSerializer
    queryset = VoiceInsights.objects.all()

    def get(self, request, user_id, year, start_month, end_month, *args, **kwargs):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        voice_insights = self.queryset.filter(
            user_id=user_id,
            year=year,
            month__gte=start_month,
            month__lte=end_month,
        )

        if not voice_insights.exists():
            return Response(
                {"message": "No voice insights data found for the given user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        managed_by = voice_insights.first().managed_by
        grade_counts = voice_insights.values("grade").annotate(count=Count("grade"))

        all_voice_insights_stats = {
            "Year": year,
            "start_month": start_month,
            "end_month": end_month,
            "managed_by": managed_by,
            "total_SPs": next(
                (item["count"] for item in grade_counts if item["grade"] == "SP"), 0
            ),
            "total_As": next(
                (item["count"] for item in grade_counts if item["grade"] == "A"), 0
            ),
            "total_Bs": next(
                (item["count"] for item in grade_counts if item["grade"] == "B"), 0
            ),
            "total_Cs": next(
                (item["count"] for item in grade_counts if item["grade"] == "C"), 0
            ),
            "total_Ds": next(
                (item["count"] for item in grade_counts if item["grade"] == "D"), 0
            ),
            "total_stats": {
                "total_aes": sum(voice_insights.values_list("aes", flat=True)),
                "total_outbound": sum(
                    voice_insights.values_list("actual_outbound_calls", flat=True)
                ),
                "total_talktime": sum(
                    voice_insights.values_list("actual_talktime", flat=True)
                ),
                "total_inbound_calls": sum(
                    voice_insights.values_list("actual_inbound_calls", flat=True)
                ),
                "total_csat": sum(voice_insights.values_list("csat", flat=True)),
                "total_overall_score": sum(
                    voice_insights.values_list("overall_score", flat=True)
                ),
            },
        }

        return Response(all_voice_insights_stats, status=status.HTTP_200_OK)
