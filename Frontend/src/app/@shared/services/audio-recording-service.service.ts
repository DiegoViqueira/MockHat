import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AudioRecordingServiceService {
  private chunks: Blob[] = [];
  private mediaRecorder!: MediaRecorder;
  private audioContext: AudioContext = new AudioContext();
  private audioBlobSubject = new Subject<Blob>();

  audioBlob$: Observable<Blob> = this.audioBlobSubject.asObservable();

  async startRecording(): Promise<void> {
    try {
      if (this.audioContext.state === 'suspended') {
        await this.audioContext.resume();
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.mediaRecorder.ondataavailable = this.handleDataAvailable.bind(this);
      this.mediaRecorder.onstop = this.handleStop.bind(this);
      this.mediaRecorder.start();
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  }

  private handleDataAvailable(event: BlobEvent): void {
    if (event.data.size > 0) {
      this.chunks.push(event.data);
    }
  }

  async stopRecording(): Promise<void> {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
    }
  }

  private async handleStop(): Promise<void> {
    try {
      const audioBlob = new Blob(this.chunks, { type: 'audio/mp3' });
      this.audioBlobSubject.next(audioBlob);
    } catch (error) {
      console.error('Error processing audio data:', error);
    } finally {
      this.chunks = [];
    }
  }
}
