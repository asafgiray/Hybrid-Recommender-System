##TR
## MovieLens Veri Kümesi Kullanarak Hibrit Öneri Sistemi
Bu proje, film bilgileri ve kullanıcı derecelendirmelerini içeren MovieLens veri kümesini kullanarak bir hibrit öneri sistemi uygular.

## Genel Bakış
Bu projenin amacı, işbirlikçi filtreleme ve içerik tabanlı filtreleme tekniklerini birleştirerek film için sağlam bir öneri sistemi oluşturmaktır. İşbirlikçi filtreleme, kullanıcı-öğe etkileşimlerini kullanarak öğeleri kullanıcı davranışı ve tercihlerine göre önerirken, içerik tabanlı filtreleme önceki beğenilmiş öğelere benzer öğeleri önermek için öğe ve kullanıcı özelliklerini analiz eder.

## Veri Kümesi
Bu projede kullanılan veri kümesi iki ana dosyadan oluşur:

movie.csv: Bu dosya, film kimlikleri, başlıkları, türleri ve diğer özellikleri gibi filmlerle ilgili bilgileri içerir.
rating.csv: Bu dosya, filmler için kullanıcı derecelendirmelerini içerir. Kullanıcı kimlikleri, film kimlikleri, derecelendirmeleri ve zaman damgaları gibi bilgiler bulunur.

## Kullanılan Teknikler

İşbirlikçi Filtreleme: İşbirlikçi filtreleme, kullanıcı-öğe etkileşimlerini kullanarak kullanıcının davranışı ve tercihlerine göre öneriler yapar.
İçerik Tabanlı Filtreleme: İçerik tabanlı filtreleme, kullanıcının önceki beğenilerine dayanarak benzer öğeleri önermek için öğe ve kullanıcı özelliklerini analiz eder.
Hibrit Yaklaşım: Sistem, işbirlikçi filtreleme ve içerik tabanlı filtreleme tekniklerini birleştirerek, hem kullanıcı tercihlerini hem de öğe özelliklerini yansıtan kişiselleştirilmiş öneriler sunar.

## Kod Yapısı
Proje yapısı aşağıdaki gibi düzenlenmiştir:

movie_lens_dataset/: MovieLens veri kümesi dosyalarını içeren dizin. movie.csv, rating.csv
hybrid_recommendation.py: Hibrit öneri sisteminin uygulanmasını içeren Python dosyası.
README.md: Bu dosya, projenin genel bir açıklamasını ve kodun nasıl çalıştırılacağına dair yönergeleri içerir.

## Katkı
Katkılar ve geri bildirimler her zaman memnuniyetle karşılanır! Herhangi bir sorun bulursanız veya iyileştirme önerileriniz varsa, lütfen bir sorun açın veya bir çekme isteği gönderin.

## ENG
## Hybrid Recommendation System Using MovieLens Dataset
This project implements a hybrid recommendation system using the MovieLens dataset, which contains movie information and user ratings.

## Overview
The aim of this project is to create a robust recommendation system for movies by combining collaborative filtering and content-based filtering techniques. Collaborative filtering recommends items based on user behavior and preferences using user-item interactions, while content-based filtering analyzes item and user features to recommend items similar to those previously liked by the user.

## Dataset
The dataset used in this project consists of two main files:

movie.csv: This file contains information about movies, including movie IDs, titles, genres, and other attributes.
rating.csv: This file contains user ratings for movies, including user IDs, movie IDs, ratings, and timestamps.

## Techniques Used
Collaborative Filtering: Collaborative filtering recommends items based on user behavior and preferences using user-item interactions.
Content-Based Filtering: Content-based filtering analyzes item and user features to recommend items similar to those previously liked by the user.
Hybrid Approach: The system combines collaborative filtering and content-based filtering techniques to provide personalized recommendations reflecting both user preferences and item attributes.

## Code Structure
The project structure is organized as follows:

movie_lens_dataset/: Directory containing the MovieLens dataset files.
movie.csv
rating.csv
hybrid_recommendation.py: Python file containing the implementation of the hybrid recommendation system.
README.md: This file provides an overview of the project and instructions for running the code.

## Contribution
Contributions and feedback are always welcome! If you encounter any issues or have improvement suggestions, please feel free to open an issue or submit a pull request.
