import { Component, effect, inject, OnInit } from '@angular/core';
import { AssessmentCorrectionStoreService } from '../../stores/assesment-correction-store.service';
import { WritingAssessmentItem } from '../../models/writing.assessmen.item.model';
import { Camera, CameraDirection, CameraResultType, CameraSource } from '@capacitor/camera';
import { ImageFile } from '../../models/image.file.model';

@Component({
  selector: 'app-writing-list',
  templateUrl: './writing-list.component.html',
  styleUrls: ['./writing-list.component.scss'],
})
export class WritingListComponent implements OnInit {

  assessmentsStore = inject(AssessmentCorrectionStoreService);
  dataSource: WritingAssessmentItem[] = [];

  constructor() {
    effect(() => {
      if (this.assessmentsStore.assessments()) {
        this.dataSource = [...this.assessmentsStore.assessments()];

      }
    });
  }

  ngOnInit() { }

  addData(item: WritingAssessmentItem) {

    this.takePicture(item.student_id ?? '');

  }


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

  async takePicture(student_id: string) {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: CameraResultType.DataUrl,
        source: CameraSource.Camera,
        direction: CameraDirection.Rear,
      });

      const capturedImage = image.dataUrl;
      if (capturedImage) {
        const file = this.dataUrlToBlob(capturedImage);
        const itemFile = { file: file, url: capturedImage };
        this.assessmentsStore.updateAssessmentFile(student_id, itemFile as ImageFile);
      }

    } catch (error) {
      console.error('Error capturing image:', error);
    }
  }

}
