import { CommonModule } from '@angular/common';
import { Component, HostBinding, Input } from '@angular/core';

@Component({
  selector: 'app-task-cycle-analysis-option',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './task-cycle-analysis-option.component.html',
  styleUrl: './task-cycle-analysis-option.component.scss'
})
export class TaskCycleAnalysisOptionComponent {
  @HostBinding('class.active')
  @Input() active: boolean = false;
  
  @Input({ required: true }) 
  settings!: {
    color: string;
    title: string;
  }
}
