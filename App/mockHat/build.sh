#!/bin/bash

npx cap sync android
ionic capacitor build android

npx cap sync ios
ionic capacitor build ios
