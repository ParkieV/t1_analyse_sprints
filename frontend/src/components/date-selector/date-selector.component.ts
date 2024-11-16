import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

type dateSelectorOption = 'today' | 'week' | 'month' | 'quart' | 'dates';

@Component({
  selector: 'app-date-selector',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './date-selector.component.html',
  styleUrl: './date-selector.component.scss',
})
export class DateSelectorComponent {
  activeOption: dateSelectorOption = 'today';

  setOption(option: dateSelectorOption) {
    this.activeOption = option;
  }
}
