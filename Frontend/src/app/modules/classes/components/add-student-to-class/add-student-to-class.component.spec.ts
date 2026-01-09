import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddStudentToClassComponent } from './add-student-to-class.component';

describe('AddStudentToClassComponent', () => {
  let component: AddStudentToClassComponent;
  let fixture: ComponentFixture<AddStudentToClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddStudentToClassComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddStudentToClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
