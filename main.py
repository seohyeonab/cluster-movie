import plotly.express as px
fig2 = px.scatter(
    work,
    x=x_feature,
    y=y_feature,
    color="유형",
    hover_name="movieNm",
    hover_data={
        "유형": True,
        "first_scrn": ":,.0f",
        "total_audi": ":,.0f",
        "days_in_top10": ":,.0f",
        "longrun_index": ":.2f",
        x_feature: True,
        y_feature: True,
    },
    labels={**FEATURE_LABELS, "유형": "영화 유형", "movieNm": "영화 제목"},
    title="선택한 속성에 따른 영화 유형"
)
fig2.update_traces(marker={"size": 8, "opacity": 0.8})
fig2.update_layout(legend_title_text="영화 유형", margin=dict(l=10, r=10, t=55, b=10))
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. 3차원 산점도")
if len(selected_features) < 3:
    st.info("3차원 산점도를 보려면 분류에 사용할 속성을 세 개 이상 선택해 주세요.")
else:
    c1, c2, c3 = st.columns(3)
    with c1:
        z_x = st.selectbox(
            "3차원 X축",
            options=selected_features,
            index=0,
            format_func=lambda x: FEATURE_LABELS[x],
            key="three_x"
        )
    with c2:
        z_y = st.selectbox(
            "3차원 Y축",
            options=selected_features,
            index=1,
            format_func=lambda x: FEATURE_LABELS[x],
            key="three_y"
        )
    with c3:
        z_z = st.selectbox(
            "3차원 Z축",
            options=selected_features,
            index=2,
            format_func=lambda x: FEATURE_LABELS[x],
            key="three_z"
        )

    fig3 = px.scatter_3d(
        work,
        x=z_x,
        y=z_y,
        z=z_z,
        color="유형",
        hover_name="movieNm",
        hover_data={
            "유형": True,
            "first_scrn": ":,.0f",
            "total_audi": ":,.0f",
            "days_in_top10": ":,.0f",
            "longrun_index": ":.2f",
        },
        labels={**FEATURE_LABELS, "유형": "영화 유형"},
        title="세 속성으로 살펴보는 영화 유형"
    )
    fig3.update_traces(marker={"size": 3, "opacity": 0.8})
    fig3.update_layout(legend_title_text="영화 유형", margin=dict(l=0, r=0, t=55, b=0))
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("그래프 안에서 마우스를 드래그하면 시점을 회전할 수 있습니다.")

st.subheader("4. 유형별 평균")
summary = (
    work.groupby("유형")
    .agg(
        편수=("movieNm", "size"),
        스크린수평균=("first_scrn", "mean"),
        누적관객평균=("total_audi", "mean"),
        **{
            "10위권일수평균": ("days_in_top10", "mean"),
            "롱런지수평균": ("longrun_index", "mean")
        }
    )
    .reindex(["㉮", "㉯", "㉰"])
    .reset_index()
    .rename(columns={
        "유형": "영화 유형",
        "스크린수평균": "스크린 수 평균",
        "누적관객평균": "누적 관객 평균",
        "10위권일수평균": "10위권 일수 평균",
        "롱런지수평균": "롱런 지수 평균"
    })
)
display_summary = summary.copy()
for col in ["스크린 수 평균", "누적 관객 평균"]:
    display_summary[col] = display_summary[col].map(lambda x: f"{x:,.1f}")
for col in ["10위권 일수 평균", "롱런 지수 평균"]:
    display_summary[col] = display_summary[col].map(lambda x: f"{x:.2f}")
display_summary["편수"] = display_summary["편수"].map(lambda x: f"{x:,}")
st.dataframe(display_summary, hide_index=True, use_container_width=True)

st.subheader("5. 유형별 누적 관객 상위 영화 5편")
for cluster_name in ["㉮", "㉯", "㉰"]:
    group = work[work["유형"] == cluster_name].sort_values("total_audi", ascending=False).head(5)
    with st.expander(f"{cluster_name} 유형 — 상위 영화 {len(group)}편", expanded=True):
        if group.empty:
            st.write("이 유형에 해당하는 영화가 없습니다.")
        else:
            top = group[["movieNm", "total_audi"]].rename(
                columns={"movieNm": "영화 제목", "total_audi": "누적 관객"}
            ).copy()
            top["누적 관객"] = top["누적 관객"].map(lambda x: f"{x:,.0f}명")
            top.insert(0, "순위", range(1, len(top) + 1))
            st.dataframe(top, hide_index=True, use_container_width=True)

st.caption(
    "분석 대상은 네 속성 중 결측값이 있거나 스크린 수·누적 관객이 0 이하이거나 첫 주 관객이 0 이하인 영화를 제외했습니다. "
    "롱런 지수는 누적 관객을 첫 주 관객으로 나눈 값이며 20을 최댓값으로 제한했습니다. "
    "유형 이름 ㉮·㉯·㉰는 누적 관객 평균이 높은 순서입니다."
)
