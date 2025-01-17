#pragma once

#include <stdlib.h>
#include <juce_audio_processors/juce_audio_processors.h>

struct ring_buffer{
    //circular buffer implementation
    size_t index;
    size_t capacity;
    float* head;    
  };

float impulse_response(size_t i);

//==============================================================================
class AudioPluginAudioProcessor final : public juce::AudioProcessor
{
public:
  //==============================================================================
  AudioPluginAudioProcessor();
  ~AudioPluginAudioProcessor() override;
  
  //==============================================================================
  void prepareToPlay (double sampleRate, int samplesPerBlock) override;
  void releaseResources() override;
  
  bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
  
  void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;
  using AudioProcessor::processBlock;
  
  //==============================================================================
  juce::AudioProcessorEditor* createEditor() override;
  bool hasEditor() const override;
  
  //==============================================================================
  const juce::String getName() const override;
  
  bool acceptsMidi() const override;
  bool producesMidi() const override;
  bool isMidiEffect() const override;
  double getTailLengthSeconds() const override;
  
  //==============================================================================
  int getNumPrograms() override;
  int getCurrentProgram() override;
  void setCurrentProgram (int index) override;
  const juce::String getProgramName (int index) override;
  void changeProgramName (int index, const juce::String& newName) override;
  
  //==============================================================================
  void getStateInformation (juce::MemoryBlock& destData) override;
  void setStateInformation (const void* data, int sizeInBytes) override;
  
  float tone_fucker(float sample, float gain, float thresh);
  
  juce::AudioParameterFloat* fuzz_gain;

  float FIR_bandpass_filter(float sample, struct ring_buffer* buffer);
  
private:
  //==============================================================================
  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (AudioPluginAudioProcessor)

  struct ring_buffer* create_ring_buffer(size_t capacity);
};

