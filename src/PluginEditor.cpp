#include "PluginProcessor.h"
#include "PluginEditor.h"
#include <iostream>

#define WIDTH 350
#define HEIGHT 650

//==============================================================================
AudioPluginAudioProcessorEditor::AudioPluginAudioProcessorEditor (AudioPluginAudioProcessor& p)
    : AudioProcessorEditor (&p), processorRef (p)
{
    juce::ignoreUnused (processorRef);

    juce::File pressed_file("C:/Users/aryan/Desktop/plugin/pedal_pressed.png");
    juce::Image pressed = juce::ImageFileFormat::loadFrom(pressed_file);

    juce::File unpressed_file("C:/Users/aryan/Desktop/plugin/pedal_unpressed.png");
    juce::Image unpressed = juce::ImageFileFormat::loadFrom(unpressed_file);

    on_off.setClickingTogglesState(true);
    on_off.setImages(false, true, false, 
        unpressed, 1.0f, juce::Colours::transparentWhite, 
        pressed, 1.0f, juce::Colours::transparentWhite, 
        pressed, 1.0f, juce::Colours::transparentWhite);

    addAndMakeVisible(on_off);

    on_off.onClick = [this] {
        if(on_off.getToggleState())
            *processorRef.fuzz_gain = fuzz_knob.getValue();
        else
            *processorRef.fuzz_gain = 0.0f;
    };

    fuzz_knob.setSliderStyle(juce::Slider::Rotary);
    fuzz_knob.setTextBoxStyle(juce::Slider::NoTextBox, false, 90, 0);
    fuzz_knob.setRange(0.0f, 20.0f, 0.01f);
    fuzz_knob.setValue(processorRef.fuzz_gain->get());

    fuzz_knob.onValueChange = [this] {
        if(on_off.getToggleState())
            *processorRef.fuzz_gain = fuzz_knob.getValue();
        else
            *processorRef.fuzz_gain = 0.0f;
    };

    addAndMakeVisible(fuzz_knob);

    setSize (WIDTH, HEIGHT);
}

AudioPluginAudioProcessorEditor::~AudioPluginAudioProcessorEditor()
{
}

//==============================================================================

bool AudioPluginAudioProcessorEditor::loadImage() {
    juce::File file("C:/Users/aryan/Desktop/plugin/background.png");
    if (file.exists())
        background = juce::ImageFileFormat::loadFrom(file);
    else
        DBG("You fucked up somehow");
    return !background.isNull();
}

void AudioPluginAudioProcessorEditor::paint (juce::Graphics& g)
{
    loadImage();
    if (background.isValid())
        g.drawImageAt(background, 0, 0);
    else
        g.fillAll(juce::Colours::black);

    g.setColour (juce::Colours::black);
    g.setFont (15.0f);
}

void AudioPluginAudioProcessorEditor::resized()
{
    fuzz_knob.setBounds(WIDTH/2 - 50, HEIGHT/2 - 50, 100, 100);
    on_off.setBounds(WIDTH / 2 - 125, 75, 250, 150);
}
