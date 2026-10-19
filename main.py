st.subheader("2. 2차원 산점도")
col_x, col_y = st.columns(2)
with col_x:
    x_feature = st.selectbox(
        "가로축 속성", selected_features,
        format_func=lambda x: FEATURE_LABELS[x], key="scatter_x"
    )
with col_y:
    y_feature = st.selectbox(
        "세로축 속성", selected_features,
        index=1, format_func=lambda x: FEATURE_LABELS[x], key="scatter_y"
    )

fig2 = px.scatter(
    work, x=x_feature, y=y_feature, color="유형", hover_name="movieNm",
    hover_data={
        "first_scrn": ":,.0f",
        "total_audi": ":,.0f",
        "days_in_top10": ":,.0f",
        "longrun_index": ":.2f",
        "유형": True,
    },
    labels={
        **FEATURE_LABELS,
        "유형": "영화 유형",
        "movieNm": "영화 제목",
        "first_scrn": "스크린 수",
        "total_audi": "누적 관객",
    },
    title="선택한 속성에 따른 영화 유형",
)
fig2.update_traces(marker={"size": 7, "opacity": 0.8})
fig2.update_layout(legend_title_text="영화 유형", margin=dict(l=10, r=10, t=55, b=10))
st.plotly_chart(fig2, use_container_width=True)

st.subheader("3. 3차원 산점도")
if len(selected_features) < 3:
    st.info("3차원 산점도를 보려면 위에서 분류 속성을 세 개 이상 선택해 주세요.")
else:
    a, b, c = st.columns(3)
    with a:
        x3 = st.selectbox("3차원 X축", selected_features, index=0,
                          format_func=lambda x: FEATURE_LABELS[x], key="x3")
    with b:
        y3 = st.selectbox("3차원 Y축", selected_features, index=1,
                          format_func=lambda x: FEATURE_LABELS[x], key="y3")
    with c:
        z3 = st.selectbox("3차원 Z축", selected_features, index=2,
                          format_func=lambda x: FEATURE_LABELS[x], key="z3")
    fig3 = px.scatter_3d(
        work, x=x3, y=y3, z=z3, color="유형", hover_name="movieNm",
        hover_data={
            "first_scrn": ":,.0f",
            "total_audi": ":,.0f",
            "days_in_top10": ":,.0f",
            "longrun_index": ":.2f",
            "유형": True,
        },
        labels={**FEATURE_LABELS, "유형": "영화 유형", "movieNm": "영화 제목"},
        title="세 속성으로 살펴보는 영화 유형",
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
        십위권일수평균=("days_in_top10", "mean"),
        롱런지수평균=("longrun_index", "mean"),
    )
    .reindex(["㉮", "㉯", "㉰"])
    .reset_index()
    .rename(columns={
        "유형": "영화 유형",
        "스크린수평균": "스크린 수 평균",
        "누적관객평균": "누적 관객 평균",
        "십위권일수평균": "10위권 일수 평균",
        "롱런지수평균": "롱런 지수 평균",
    })
)
show_summary = summary.copy()
show_summary["편수"] = show_summary["편수"].map(lambda v: f"{v:,}")
for col in ["스크린 수 평균", "누적 관객 평균"]:
    show_summary[col] = show_summary[col].map(lambda v: f"{v:,.1f}")
for col in ["10위권 일수 평균", "롱런 지수 평균"]:
    show_summary[col] = show_summary[col].map(lambda v: f"{v:.2f}")
st.dataframe(show_summary, hide_index=True, use_container_width=True)

st.subheader("5. 유형별 누적 관객 상위 영화 5편")
for label in ["㉮", "㉯", "㉰"]:
    group = work[work["유형"] == label].sort_values("total_audi", ascending=False).head(5)
    with st.expander(f"{label} 유형", expanded=True):
        if group.empty:
            st.write("해당 유형에 영화가 없습니다.")
        else:
            top = group[["movieNm", "total_audi"]].rename(
                columns={"movieNm": "영화 제목", "total_audi": "누적 관객"}
            ).copy()
            top.insert(0, "순위", range(1, len(top) + 1))
            top["누적 관객"] = top["누적 관객"].map(lambda v: f"{v:,.0f}명")
            st.dataframe(top, hide_index=True, use_container_width=True)

st.caption(
    "결측값이 있거나 스크린 수·누적 관객이 0 이하인 영화, 첫 주 관객이 0 이하인 영화는 제외했습니다. "
    "롱런 지수는 누적 관객 ÷ 첫 주 관객이며 최대 20으로 제한했습니다. "
    "유형 ㉮·㉯·㉰는 누적 관객 평균이 높은 순서입니다."
)
