#pragma once  // include only once
#include <Arduino.h>
#include <ESP_I2S.h> // drives I2S audio port

#include "sound_setup.h" // four files made by 'wav2header.py'
#include "sound_nap.h"
#include "sound_feed.h"
#include "sound_pet.h"

const int AUDIO_BCLK_PIN = 10; // ESP D10 
const int AUDIO_LRC_PIN = 20; // ESP D7
const int AUDIO_DIN_PIN = 21; // ESP D6

// must match rate in 'wav2header.py'
const uint32_t AUDIO_SAMPLE_RATE = 16000;
const float AUDIO_VOLUME = 0.6f; // should be below 0.7 for 1W speaker

struct Sound { 
    const int16_t *samples; // where samples start in flash
    size_t length;
};

I2SClass audioOut;  // I2S port object
QueueHandle_t soundQueue = nullptr; //  queue isn't made yet
bool audioReady = false;

const size_t AUDIO_CHUNK_SAMPLES = 256; // samples sent to amp at a time

void audioTask(void *unused){ //FreeRTOS task, runs alongside loop()
    static int16_t chunk[AUDIO_CHUNK_SAMPLES]; // buffer for one chunk (samples)
    Sound sound; // stores received sound request

    while (true) { // loops forever
        xQueueReceive(soundQueue, &sound, portMAX_DELAY); // copies items into sound

        size_t position = 0; // in track
        while (position < sound.length) { // continues till all samples sent
            if (uxQueueMessagesWaiting(soundQueue) > 0){ 
                break; // new action cuts off old sound
            }

            size_t count = sound.length - position;
            if(count > AUDIO_CHUNK_SAMPLES) { // send fewer samples for last chunk
                count = AUDIO_CHUNK_SAMPLES;
            }
            for (size_t i = 0; i < count; i++) {
                chunk[i] = static_cast<int16_t>(sound.samples[position + i] * AUDIO_VOLUME); // copies next samples from flash
            } // and applies volume, converts float to int

            // treats 16-bit samples as bytes
            // waits until there's room in buffer
            audioOut.write(reinterpret_cast<uint8_t *>(chunk), count * sizeof(int16_t));
            position += count;

        }
        
        if (uxQueueMessagesWaiting(soundQueue) == 0) {
            memset(chunk, 0, sizeof(chunk)); // sends zeroes if no new sound
            for (int i = 0; i < 12; i++){ // 12 times
                audioOut.write(reinterpret_cast<uint8_t *>(chunk), sizeof(chunk));
            }
        }   
    }
}

void setUpAudio() {
    audioOut.setPins(AUDIO_BCLK_PIN, AUDIO_LRC_PIN, AUDIO_DIN_PIN); // I2S pins to use
    if (!audioOut.begin(I2S_MODE_STD, AUDIO_SAMPLE_RATE, I2S_DATA_BIT_WIDTH_16BIT,
                        I2S_SLOT_MODE_MONO)) {// starts I2S hardware
    Serial.println("Amp not starting"); // failure msg
    return;
    }

    soundQueue = xQueueCreate(1, sizeof(Sound)); // room for 1 item, size of Sound struct
    xTaskCreate(audioTask, "audio", 4096, nullptr, 2, nullptr); // starts background task
    audioReady = true;
}

void playSound(const int16_t *samples, size_t length){
    if(!audioReady) {
        return;
    }
    Sound sound = {samples, length};
    xQueueOverwrite(soundQueue, &sound); // replaces anything not yet started
}

void playSetupSound() {playSound(SOUND_SETUP, SOUND_SETUP_LENGTH); }
void playNapSound()   {playSound(SOUND_NAP, SOUND_NAP_LENGTH); }
void playFeedSound() {playSound(SOUND_FEED, SOUND_FEED_LENGTH); }
void playPetSound() {playSound(SOUND_PET, SOUND_PET_LENGTH); }




