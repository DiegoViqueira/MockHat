import { Component, inject, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Camera, CameraDirection, CameraResultType, CameraSource } from '@capacitor/camera';
import { WritingService } from '../../services/writing.service';
import { WritingTask } from '../../models/writing.task.model';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Level } from '../../models/user-level.enum';
import { TaskByLevel } from '../../shared/common-environments';
import { AssessmentCorrectionStoreService } from '../../stores/assesment-correction-store.service';
import { WritingAssessmentItemState } from '../../models/writing.assessment.item.state.model';


@Component({
  selector: 'app-wirting',
  templateUrl: './wirting.page.html',
  styleUrls: ['./wirting.page.scss'],
})
export class WirtingPage implements OnInit {
  public folder!: string;
  private activatedRoute = inject(ActivatedRoute);
  private service = inject(WritingService);
  private assessmentsStore = inject(AssessmentCorrectionStoreService);

  capturedImage: string | undefined;
  spinnerLoading = false;
  private _formBuilder = inject(FormBuilder);
  writingForm: FormGroup;

  protected readonly levels = TaskByLevel;
  filteredTasks: WritingTask[] = [];


  constructor() {
    this.writingForm = this._formBuilder.group({
      task: [WritingTask.Email],
      level: [Level.B1],
      text_question: ['', Validators.required],
    });
    this.onLevelChange(Level.B1);
  }

  ngOnInit() {
    this.folder = this.activatedRoute.snapshot.paramMap.get('id') as string;
  }



  steps = ['writing.upload_assessment', 'writing.upload_answer', 'writing.evaluate'];
  currentStep = 0;

  nextStep() {
    if (this.currentStep < this.steps.length - 1) {
      this.currentStep++;
    }

    const isLastStep = this.currentStep === this.steps.length - 1;
    if (isLastStep) {
      this.assessmentsStore.assessments()?.forEach((assessment) => {
        if (assessment.file) {
          this.service
            .evaluate(
              assessment.student_id ?? '',
              this.writingForm.get('level')?.value,
              this.writingForm.get('text_question')?.value,
              this.writingForm.get('task')?.value,
              assessment.file.file ?? new Blob()
            )
            .subscribe({
              next: (response) => {
                this.assessmentsStore.updateState(
                  assessment.student_id ?? '',
                  WritingAssessmentItemState.Completed,
                  response
                );
              },
              error: (err) => {
                const errorMessage = err?.message || ''; // Safely access the 'message' property
                const errorType = errorMessage.includes('error.license')
                  ? WritingAssessmentItemState.LimitReached
                  : WritingAssessmentItemState.Error;
                this.assessmentsStore.updateState(assessment.student_id ?? '', errorType, undefined);
              },
            });
        } else {
          this.assessmentsStore.removeItem(assessment.student_id ?? '');
        }
      });

    }
  }

  prevStep() {
    if (this.currentStep > 0) {
      this.currentStep--;
    }
  }

  goFirst() {
    this.currentStep = 0;
    this.onLevelChange(Level.B1);
    this.writingForm.reset();
  }

  async takePicture() {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.DataUrl,
        source: CameraSource.Camera,
        direction: CameraDirection.Rear,
      });

      this.capturedImage = image.dataUrl;
      if (this.capturedImage) {
        const file = this.dataUrlToBlob(this.capturedImage);
        this.spinnerLoading = true;
        this.service.translateTask(file, WritingTask.Email).subscribe({
          next: (v) => this.writingForm.patchValue({ text_question: v }),
          error: (e) => console.error(e),
          complete: () => this.spinnerLoading = false,
        });
      }

    } catch (error) {
      console.error('Error capturing image:', error);
    }
  }

  // Helper function to convert Data URL to Blob
  dataUrlToBlob(dataUrl: string): Blob {
    const [header, base64] = dataUrl.split(',');
    const mimeType = header.match(/:(.*?);/)![1]; // Extract MIME type
    const byteString = window.atob(base64);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uint8Array = new Uint8Array(arrayBuffer);

    for (let i = 0; i < byteString.length; i++) {
      uint8Array[i] = byteString.charCodeAt(i);
    }

    return new Blob([arrayBuffer], { type: mimeType });
  }


  onLevelChange(selectedLevel: Level) {
    const selectedLevelData = TaskByLevel.find((levelData) => levelData.level === selectedLevel);
    this.assessmentsStore.selectByLevel(selectedLevel);
    this.filteredTasks = selectedLevelData ? selectedLevelData.tasks : [];
    const firstTask = this.filteredTasks[0] || null;
    this.writingForm.get('task')?.setValue(firstTask);
  }



}
