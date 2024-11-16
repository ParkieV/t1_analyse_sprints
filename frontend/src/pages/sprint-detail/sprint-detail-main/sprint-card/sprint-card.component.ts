import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-sprint-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sprint-card.component.html',
  styleUrl: './sprint-card.component.scss',
})
export class SprintCardComponent {
  @Input({ required: true }) title!: string;

  @Input({ required: true }) value!: string;

  @Input() color: 'dark' | 'green' = 'dark';
}
