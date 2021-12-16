import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThresholdSegmentationComponent } from './threshold-segmentation.component';

describe('ThresholdSegmentationComponent', () => {
  let component: ThresholdSegmentationComponent;
  let fixture: ComponentFixture<ThresholdSegmentationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ThresholdSegmentationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ThresholdSegmentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
