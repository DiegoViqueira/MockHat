import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddTeacherToClassComponent } from './add-teacher-to-class.component';

describe('AddTeacherToClassComponent', () => {
  let component: AddTeacherToClassComponent;
  let fixture: ComponentFixture<AddTeacherToClassComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddTeacherToClassComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddTeacherToClassComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
