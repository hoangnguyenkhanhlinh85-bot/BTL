import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

DATA_FILES = {
    'users': 'users.csv',
    'movies': 'movies.csv',
    'genres': 'genres.csv',
    'movie_genres': 'movie_genres.csv',
    'ratings': 'ratings.csv',
    'subscriptions': 'subscriptions.csv'
}


def generate_data(seed=None):
    if seed is None:
        seed = 42
    np.random.seed(seed)
    random.seed(seed)

    users = pd.DataFrame({
        'user_id': range(1, 21),
        'age': np.random.randint(18, 60, 20),
        'gender': np.random.choice(['Nam', 'Nu'], 20),
        'location': np.random.choice(['Ha Noi', 'TP HCM', 'Da Nang'], 20)
    })

    movies = pd.DataFrame({
        'movie_id': range(1, 16),
        'title': [
            'Inception', 'The Matrix', 'Interstellar', 'The Dark Knight', 'Avengers',
            'Titanic', 'The Notebook', 'La La Land', 'A Star is Born', 'Romeo + Juliet',
            'The Conjuring', 'It', 'Annabelle', 'Get Out', 'A Quiet Place'
        ],
        'release_year': np.random.randint(2000, 2024, 15),
        'production_cost': np.random.uniform(5000, 50000, 15).round(2)
    })

    genres = pd.DataFrame({
        'genre_id': [1, 2, 3, 4, 5],
        'genre_name': ['Hanh dong', 'Vien tuong', 'Lang man', 'Kinh di', 'Tam ly']
    })

    mg_data = []
    for m_id in movies['movie_id']:
        selected_genres = random.sample([1, 2, 3, 4, 5], random.randint(1, 2))
        for g_id in selected_genres:
            mg_data.append({'movie_id': m_id, 'genre_id': g_id})
    movie_genres = pd.DataFrame(mg_data)

    r_data = {'user_id': [], 'movie_id': [], 'rating': [], 'timestamp': []}
    for _ in range(120):
        u, m = random.randint(1, 20), random.randint(1, 15)
        r_data['user_id'].append(u)
        r_data['movie_id'].append(m)
        r_data['rating'].append(random.choice([3, 4, 5]))
        r_data['timestamp'].append(
            (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 100))).strftime('%Y-%m-%d')
        )
    ratings = pd.DataFrame(r_data).drop_duplicates(subset=['user_id', 'movie_id'])

    subs_data = []
    for u in users['user_id']:
        plan = random.choice(['Basic', 'Premium'])
        price = 100000 if plan == 'Basic' else 200000
        subs_data.append({
            'user_id': u,
            'plan_type': plan,
            'amount': price,
            'payment_date': '2024-03-01'
        })
    subscriptions = pd.DataFrame(subs_data)

    users.to_csv(DATA_FILES['users'], index=False)
    movies.to_csv(DATA_FILES['movies'], index=False)
    genres.to_csv(DATA_FILES['genres'], index=False)
    movie_genres.to_csv(DATA_FILES['movie_genres'], index=False)
    ratings.to_csv(DATA_FILES['ratings'], index=False)
    subscriptions.to_csv(DATA_FILES['subscriptions'], index=False)

    return {
        'users': users,
        'movies': movies,
        'genres': genres,
        'movie_genres': movie_genres,
        'ratings': ratings,
        'subscriptions': subscriptions
    }


@st.cache_data
def load_data():
    for path in DATA_FILES.values():
        if not os.path.exists(path):
            return None
    return {name: pd.read_csv(path) for name, path in DATA_FILES.items()}


def ensure_data():
    data = load_data()
    if data is None:
        data = generate_data()
    return data


def make_csv_download(df, filename):
    return df.to_csv(index=False).encode('utf-8')


def prepare_analysis(data):
    ratings = data['ratings']
    movies = data['movies']
    genres = data['genres']
    movie_genres = data['movie_genres']
    subscriptions = data['subscriptions']
    users = data['users']

    movies_with_ratings = (
        ratings.groupby('movie_id')
        .agg(avg_rating=('rating', 'mean'), rating_count=('rating', 'count'))
        .reset_index()
        .merge(movies[['movie_id', 'title']], on='movie_id', how='left')
    )
    top_movies = movies_with_ratings.sort_values(
        by=['avg_rating', 'rating_count'], ascending=[False, False]
    ).head(5)

    rating_counts = ratings['rating'].value_counts().sort_index()
    plan_counts = subscriptions['plan_type'].value_counts()
    revenue_by_plan = subscriptions.groupby('plan_type')['amount'].sum()
    total_revenue = subscriptions['amount'].sum()
    avg_rating = ratings['rating'].mean()
    genre_counts = (
        movie_genres.merge(genres, on='genre_id')
        .genre_name.value_counts()
    )
    age_groups = pd.cut(
        users['age'], bins=[17, 24, 34, 44, 54, 64], labels=['18-24', '25-34', '35-44', '45-54', '55+']
    ).value_counts().sort_index()
    location_counts = users['location'].value_counts()

    return {
        'top_movies': top_movies,
        'rating_counts': rating_counts,
        'plan_counts': plan_counts,
        'revenue_by_plan': revenue_by_plan,
        'total_revenue': total_revenue,
        'avg_rating': avg_rating,
        'genre_counts': genre_counts,
        'age_groups': age_groups,
        'location_counts': location_counts
    }


def main():
    st.set_page_config(page_title='Mini Netflix Streamlit', layout='wide')

    st.title('Mini Netflix Data Web (Streamlit)')
    st.write('Web app này hiển thị dữ liệu mẫu, phân tích chi tiết và các biểu đồ đẹp hơn.')

    data = ensure_data()
    analysis = prepare_analysis(data)
    dataset_names = list(data.keys())

    if st.sidebar.button('Tạo lại dữ liệu'):
        st.cache_data.clear()
        data = generate_data(seed=random.randint(0, 999999))
        analysis = prepare_analysis(data)
        st.success('Dữ liệu đã được tạo lại.')

    selected = st.sidebar.selectbox('Chọn dataset', dataset_names, index=0)
    st.sidebar.markdown('---')
    st.sidebar.write('Các dataset hiện có:')
    for name in dataset_names:
        st.sidebar.write(f'- **{name}**: {len(data[name])} bản ghi')

    st.subheader('Tổng quan nhanh')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Người dùng', len(data['users']))
    col2.metric('Phim', len(data['movies']))
    col3.metric('Đánh giá trung bình', f'{analysis["avg_rating"]:.2f}')
    col4.metric('Doanh thu gói', f'{analysis["total_revenue"]:,} VND')

    st.markdown('---')
    st.subheader('Biểu đồ phân tích')
    c1, c2 = st.columns(2)
    c1.write('**Phân bố điểm đánh giá**')
    c1.bar_chart(analysis['rating_counts'])
    c2.write('**Số lượng phim theo thể loại**')
    c2.bar_chart(analysis['genre_counts'])

    c3, c4 = st.columns(2)
    c3.write('**Tỷ lệ gói đăng ký**')
    c3.bar_chart(analysis['plan_counts'])
    c4.write('**Doanh thu theo gói**')
    c4.bar_chart(analysis['revenue_by_plan'])

    st.markdown('---')
    with st.expander('Chi tiết người dùng'): 
        u1, u2 = st.columns(2)
        u1.write('Tuổi người dùng')
        u1.bar_chart(analysis['age_groups'])
        u2.write('Địa điểm người dùng')
        u2.bar_chart(analysis['location_counts'])

    st.markdown('---')
    st.subheader('Top 5 phim theo điểm đánh giá')
    st.table(
        analysis['top_movies'][['title', 'avg_rating', 'rating_count']]
        .assign(avg_rating=lambda df: df['avg_rating'].round(2))
        .rename(columns={
            'title': 'Tên phim',
            'avg_rating': 'Điểm TB',
            'rating_count': 'Số lượng đánh giá'
        })
    )

    st.markdown('---')
    st.header(selected.replace('_', ' ').title())
    st.write(f'Tổng số bản ghi: {len(data[selected])}')

    st.dataframe(data[selected])

    csv_bytes = make_csv_download(data[selected], f'{selected}.csv')
    st.download_button(
        label='Tải CSV',
        data=csv_bytes,
        file_name=f'{selected}.csv',
        mime='text/csv'
    )

    with st.expander('Xem thông tin các dataset khác'):
        for name in dataset_names:
            st.write(f'**{name}**: {len(data[name])} bản ghi')


if __name__ == '__main__':
    main()