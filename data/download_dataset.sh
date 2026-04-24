#!/usr/bin/env bash
set -euo pipefail


# conf
BASE_DIR="$(dirname "$(realpath "$0")")/ISIC2018"
mkdir -p "$BASE_DIR"

# URLs
TRAIN_DATA="https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1-2_Training_Input.zip"
TRAIN_GT="https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Training_GroundTruth.zip"
VAL_DATA="https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1-2_Validation_Input.zip"
VAL_GT="https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Validation_GroundTruth.zip"
TEST_DATA="https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1-2_Test_Input.zip"
TEST_GT="https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Test_GroundTruth.zip"


# download f
download_one() {
    local key="$1"
    local url="$2"

    local zip="$BASE_DIR/${key}.zip"
    local target="$BASE_DIR/$key"

    # skip alredz downloaded ones
    if [[ -d "$target" && -n "$(ls -A "$target" 2>/dev/null)" ]]; then
        echo "[SKIP] $key"
        return
    fi

    mkdir -p "$target"

    echo "[DOWNLOAD] $key"
    wget -q --show-progress -O "$zip" "$url"

    # zip check and retry if corrupt
    if ! unzip -t "$zip" >/dev/null 2>&1; then
        echo "[CORRUPT ZIP → RETRY] $key"
        rm -f "$zip"
        wget -q --show-progress -O "$zip" "$url"

        if ! unzip -t "$zip" >/dev/null 2>&1; then
            echo "[ERROR] $key failed after retry"
            exit 1
        fi
    fi

    # unzip and flatten if needed
    echo "[EXTRACT] $key"
    unzip -q "$zip" -d "$target"

    inner=$(find "$target" -mindepth 1 -maxdepth 1 -type d | head -n 1)

    if [[ -n "${inner:-}" ]]; then
        mv "$inner"/* "$target"/ 2>/dev/null || true
        rm -rf "$inner"
    fi

    rm -f "$zip"
    echo "[DONE] $key"
}



echo "Starting downloads..."

download_one "training-data" "$TRAIN_DATA" &
download_one "training-ground-truth" "$TRAIN_GT" &
download_one "validation-data" "$VAL_DATA" &
download_one "validation-ground-truth" "$VAL_GT" &
download_one "test-data" "$TEST_DATA" &
download_one "test-ground-truth" "$TEST_GT" &

wait

echo "DONE"
