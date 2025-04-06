#!/bin/bash

# Clé API et symbole Apple
API_KEY="cvpde31r01qve7io8q5gcvpde31r01qve7io8q60"
SYMBOL="AAPL"

# URL de l'API Finnhub 
URL="https://finnhub.io/api/v1/quote?symbol=$SYMBOL&token=$API_KEY"

# Fichier CSV pour les datas
OUTPUT_FILE="AAPL_data.csv"

# Vérifier si le fichier de sortie existe
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "timestamp,price" > "$OUTPUT_FILE"
fi

# Récupérer les données de l'API
response=$(curl -s "$URL")

# Extraire le prix actuel à l'aide de jq
current_price=$(echo "$response" | jq '.c')

# Vérifier si le prix est valide
if [ "$current_price" != "null" ]; then
    timestamp=$(date --iso-8601=seconds)
    echo "$timestamp,$current_price" >> "$OUTPUT_FILE"
    echo "Données enregistrées : $timestamp, $current_price"
else
    echo "Erreur lors de la récupération des données."
fi
