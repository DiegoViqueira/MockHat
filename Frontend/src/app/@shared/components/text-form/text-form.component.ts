import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'wlk-text-form',
    templateUrl: './text-form.component.html',
    styleUrl: './text-form.component.scss',
    standalone: false
})
export class TextFormComponent {
  @Output() responseCompleted = new EventEmitter<string>();

  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      response_text: ['', Validators.required],
    });
  }

  response() {
    const responseText = this.form.get('response_text')?.value;
    this.responseCompleted.emit(responseText);
  }
}
