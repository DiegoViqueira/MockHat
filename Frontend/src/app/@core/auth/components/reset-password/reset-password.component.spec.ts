import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPasswordValidationComponent } from './reset-password.component';

describe('ResetPasswordValidationComponent', () => {
  let component: ResetPasswordValidationComponent;
  let fixture: ComponentFixture<ResetPasswordValidationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResetPasswordValidationComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ResetPasswordValidationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
