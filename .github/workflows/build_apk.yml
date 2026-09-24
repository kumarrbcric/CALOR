name: Build CalorPulse APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flet "flet[all]"

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.22.x'
          channel: 'stable'

      - name: Build Android APK
        run: |
          flet build apk

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: CalorPulse-Android-APK
          path: build/apk/*.apk
