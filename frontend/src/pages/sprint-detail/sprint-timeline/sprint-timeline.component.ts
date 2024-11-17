import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { SprintDetailService } from '../sprint-detail.service';
import { NgxSliderModule, Options } from '@angular-slider/ngx-slider';
import { Sprint } from '../../../models/sprint.model';
import { filter } from 'rxjs';
import { CommonModule } from '@angular/common';

function dayRange(firstDate: Date, secondDate: Date) {
  const oneDay = 24 * 60 * 60 * 1000;
  const diffDays = Math.round(
    Math.abs((firstDate.getTime() - secondDate.getTime()) / oneDay)
  );
  return diffDays;
}

const getDaysArray = (start: Date, end: Date) => {
  const arr = [];
  for (
    const dt = new Date(start);
    dt <= new Date(end);
    dt.setDate(dt.getDate() + 1)
  ) {
    arr.push(new Date(dt));
  }
  return arr;
};

@Component({
  selector: 'app-sprint-timeline',
  standalone: true,
  imports: [CommonModule, NgxSliderModule],
  templateUrl: './sprint-timeline.component.html',
  styleUrl: './sprint-timeline.component.scss',
})
export class SprintTimelineComponent {
  get filters() {
    return this._sprintDetailService.filters;
  }

  minValue: number = 0;

  maxValue: number = 0;

  options?: Options;

  updateSprint() {
    debugger;
    const days = getDaysArray(
      new Date(this._sprintDetailService.sprint.sprintStartDate),
      new Date(this._sprintDetailService.sprint.sprintEndDate)
    );
    let i = 0;
    this.minValue = 0;
    this.options = {
      showTicksValues: true,
      stepsArray: days.map((day) => {
        return {
          value: i++,
          legend: day.toLocaleDateString(),
        };
      }),
    };
    debugger;
    this.maxValue = i;
    this._cdr.detectChanges();
  }

  constructor(
    private _sprintDetailService: SprintDetailService,
    private _cdr: ChangeDetectorRef
  ) {
    this._sprintDetailService.loads
      .pipe(filter((res) => !res))
      .subscribe((res) => {
        this.updateSprint();
        // this.sprint =
      });
  }
}
