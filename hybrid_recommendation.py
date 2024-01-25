# PROJE: Hybrid Recommender System

# ID'si verilen kullanıcı için item-based ve user-based recomennder yöntemlerini kullanarak tahmin yapınız.
# 5 öneri user-based modelden 5 öneri de item-based modelden ele alınız ve nihai olarak 10 öneriyi 2 modelden yapınız.


#############################################
# Görev 1: Verinin Hazırlanması
#############################################
import pandas as pd
pd.pandas.set_option('display.max_columns', None)
pd.pandas.set_option('display.width', 300)

# Adım 1: Movie ve Rating veri setlerini okutunuz.

# movieId, film adı ve filmin tür bilgilerini içeren veri seti
movie = pd.read_csv('movie_lens_dataset/movie.csv')
movie.head()
movie.shape

# UserID, film adı, filme verilen oy ve zaman bilgisini içeren veri seti
rating = pd.read_csv('movie_lens_dataset/rating.csv')
rating.head()
rating.shape
rating["userId"].nunique() #benzersiz kullanıcı sayısı (138493 adet kayıtlı kullanıcı var)

# Adım 2: Rating veri setine filmlerin isimlerini ve türünü movie film setini kullanarak ekleyiniz.

# Ratingdeki kullanıcıların oy kullandıkları filmlerin sadece id'si var.
# Idlere ait film isimlerini ve türünü movie veri setinden ekliyoruz.
df = movie.merge(rating, how="left", on="movieId")
df.head()
df.shape

# Adım 3: Her bir film için toplam kaç kişinin oy kullandığını hesaplayınız.Toplam oy kullanılma sayısı 1000'un altında olan filmleri veri setinden çıkarınız.

# Her bir film için toplam kaç kişinin oy kullanıldığını hesaplıyoruz.
comment_counts_value = df["title"].value_counts()
comment_counts_value.describe()
comment_counts_value.quantile(0.92) # 1793 ~ 1800

comment_counts = pd.DataFrame(df["title"].value_counts()) #title - value counts değerlerini tutan yeni dataframe oluşturduk
comment_counts

# Toplam oy kullanılma sayısı 1800'in altında olan filmlerin isimlerini rare_movies de tutuyoruz ve veri setinden çıkartıyoruz
rare_movies = comment_counts[comment_counts["title"] <= 1800].index
rare_movies.shape #toplamda 25085 adet film var, DİKKAT -> rare_movies filmlerin title değerini tutuyor

common_movies = df[~df["title"].isin(rare_movies)] #title değeri rare_movies içinde olmayanları aldık
common_movies.head()
common_movies.shape

# Adım 4: Index'te userID'lerin sutunlarda film isimlerinin ve değer olarakta ratinglerin bulunduğu
# dataframe için pivot table oluşturunuz.

user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
user_movie_df.head()

# Adım 5: Yukarıda yapılan tüm işlemleri fonksiyonlaştıralım
def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1800].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()


#############################################
# Görev 2: Öneri Yapılacak Kullanıcının İzlediği Filmlerin Belirlenmesi
#############################################

# Adım 1: Rastgele bir kullanıcı id'si seçiniz.
random_user = 108170

# Adım 2: Seçilen kullanıcıya ait gözlem birimlerinden oluşan random_user_df adında yeni bir dataframe oluşturunuz.
random_user_df = user_movie_df[user_movie_df.index == random_user]
random_user_df.head()
random_user_df.shape #(1, 2177) yani random_user kişisinin 2177 film hakkında oy değeri (boş olanlarda sayılıyor)

# Adım 3: Seçilen kullanıcının oy kullandığı filmleri movies_watched adında bir listeye atayınız.
movies_watched = random_user_df.columns[random_user_df.notna().any()].to_list()
movies_watched

movie.columns[movie.notna().any()].to_list() #??


#############################################
# Görev 3: Aynı Filmleri İzleyen Diğer Kullanıcıların Verisine ve Id'lerine Erişmek
#############################################

# Adım 1: Seçilen kullanıcının izlediği fimlere ait sutunları user_movie_df'ten seçiniz ve movies_watched_df adında yeni bir dataframe oluşturuyoruz.
movies_watched_df = user_movie_df[movies_watched]
movies_watched_df.head()
movies_watched_df.shape

# Adım 2: Her bir kullancının seçili user'in izlediği filmlerin kaçını izlediği bilgisini taşıyan user_movie_count adında yeni bir dataframe oluşturunuz.
# Ve yeni bir df oluşturuyoruz.
user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count.head(5)
user_movie_count.describe()

len(movies_watched) #seçilen kullanıcının yorum yaptığı toplam film sayısı (183)

# Adım 3: Seçilen kullanıcının oy verdiği filmlerin yüzde 60 ve üstünü izleyenleri benzer kullanıcılar olarak görüyoruz.
# Bu kullanıcıların id’lerinden users_same_movies adında bir liste oluşturunuz.
perc = len(movies_watched) * 60 / 100 #110 adet film
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
len(users_same_movies) #kullanıcı ile %60 oranında aynı filmleri izleyen kullanıcılar


#############################################
# Görev 4: Öneri Yapılacak Kullanıcı ile En Benzer Kullanıcıların Belirlenmesi
#############################################

# Adım 1: user_same_movies listesi içerisindeki seçili user ile benzerlik gösteren kullanıcıların id’lerinin bulunacağı şekilde movies_watched_df dataframe’ini filtreleyiniz.
final_df = movies_watched_df[movies_watched_df.index.isin(users_same_movies)] #kullanıcının izlediği film df'ini filtreledik
final_df.head()
final_df.shape

# Adım 2: Kullanıcıların birbirleri ile olan korelasyonlarının bulunacağı yeni bir corr_df dataframe’i oluşturunuz.
corr_df = final_df.T.corr().unstack().sort_values()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()

corr_df[corr_df["user_id_1"] == random_user] #userid_1 olan kolon seçtiğimiz user olacak sadece, filtreledik

# Adım 3: Seçili kullanıcı ile yüksek korelasyona sahip (0.65’in üzerinde olan) kullanıcıları filtreleyerek top_users adında yeni bir dataframe oluşturunuz.
top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][["user_id_2", "corr"]].reset_index(drop=True)
top_users = top_users.sort_values(by='corr', ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)
top_users.shape
top_users

# Adım 4:  top_users dataframe’ine rating veri seti ile merge ediniz
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]
top_users_ratings["userId"].unique()
top_users_ratings


#############################################
# Görev 5: Weighted Average Recommendation Score'un Hesaplanması ve İlk 5 Filmin Tutulması
#############################################

# Adım 1: Her bir kullanıcının corr ve rating değerlerinin çarpımından oluşan weighted_rating adında yeni bir değişken oluşturunuz.
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings

# Adım 2: Film id’sive her bir filme ait tüm kullanıcıların weighted rating’lerinin ortalama değerini içeren recommendation_df adında yeni bir
# dataframe oluşturunuz.
recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()
recommendation_df.head()

# Adım 3: Adım3: recommendation_df içerisinde weighted rating'i 3.5'ten büyük olan filmleri seçiniz ve weighted rating’e göre sıralayınız.
# İlk 5 gözlemi movies_to_be_recommend olarak kaydediniz.
recommendation_df[recommendation_df["weighted_rating"] > 3.5]
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)


# Adım 4:  Tavsiye edilen 5 filmin isimlerini getiriniz.
movies_to_be_recommend.merge(movie[["movieId", "title"]])["title"][:10]

# 0     Mystery Science Theater 3000: The Movie (1996)
# 1                          Christmas Story, A (1983)
# 2                                Natural, The (1984)
# 3                              Super Troopers (2001)
# 4       Anchorman: The Legend of Ron Burgundy (2004)
# 5                         Princess Bride, The (1987)
# 6    Violent Cop (Sono otoko, kyôbô ni tsuki) (1989)
# 7                        The Raid: Redemption (2011)
# 8                                    Watchmen (2009)
# 9                              28 Weeks Later (2007)


#############################################
# Görev 6: Item-Based Recommendation
#############################################

# Kullanıcının en son izlediği ve en yüksek puan verdiği filmin adına göre item-based öneri yapınız.
user = 108170

# Adım 1: movie,rating veri setlerini okutunuz.
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')

# Adım 2: Öneri yapılacak kullanıcının 5 puan verdiği filmlerden puanı en güncel olan filmin id'sinin alınız.
movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)].sort_values(by="timestamp", ascending=False)["movieId"][0:5].values[1] #liste olarak döndürdüğü için sadece bir değer çektik

# Adım 3 :User based recommendation bölümünde oluşturulan user_movie_df dataframe’ini seçilen film id’sine göre filtreleyiniz.
movie[movie["movieId"] == movie_id]["title"].values[0]
movie_df = user_movie_df[movie[movie["movieId"] == movie_id]["title"].values[0]]
movie_df

# Adım 4: Filtrelenen dataframe’i kullanarak seçili filmle diğer filmlerin korelasyonunu bulunuz ve sıralayınız.
user_movie_df.corrwith(movie_df).sort_values(ascending=False).head(10)

# Son iki adımı uygulayan fonksiyon
def item_based_recommender(movie_name, user_movie_df):
    movie = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)

# Adım 5: Seçili film’in kendisi haricinde ilk 5 film’I öneri olarak veriniz.
movies_from_item_based = item_based_recommender(movie[movie["movieId"] == movie_id]["title"].values[0], user_movie_df)
# 1'den 6'ya kadar. 0'da filmin kendisi var. Onu dışarda bıraktık.
movies_from_item_based[1:6].index

# Requiem for a Dream (2000)                       0.335476
# Monster's Ball (2001)                            0.333522
# 21 Grams (2003)                                  0.321224
# In the Mood For Love (Fa yeung nin wa) (2000)    0.320119
# Boogie Nights (1997)                             0.318249
# Touching the Void (2003)                         0.310872
# Into the Wild (2007)                             0.308647
# In the Bedroom (2001)                            0.306308
# Machinist, The (Maquinista, El) (2004)           0.299770