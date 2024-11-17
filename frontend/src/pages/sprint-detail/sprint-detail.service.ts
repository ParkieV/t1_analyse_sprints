import { Injectable } from '@angular/core';
import { SprintsService } from '../../services/sprints.service';
import { BehaviorSubject, Subject } from 'rxjs';
import { SprintDetail, SprintEntity } from '../../models/sprint.model';
import { FormControl, FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root',
})
export class SprintDetailService {
  sprintId!: string;

  sprint!: SprintDetail;

  loads = new BehaviorSubject<boolean>(false);

  kanban: { status: string; tasks: SprintEntity[] }[] = [];

  filters = new FormGroup({
    startDate: new FormControl(),
    endDate: new FormControl(),
  });

  priority: { [key: string]: number } = {
    Создано: 1,
    Анализ: 2,
    'В работе': 3,
    Разработка: 4,
    Тестирование: 5,
    'Подтверждение исправления': 6,
    Исправление: 7,
    Выполнено: 8,
    Закрыто: 9,
    'Отклонён исполнителем': 10,
    'Отклонен исполнителем': 10,
    Отложен: 11,
    СТ: 12,
    'СТ Завершено': 13,
    Подтверждение: 14,
    Локализация: 15,
  };

  constructor(private readonly _sprintsService: SprintsService) {}

  getSprint() {
    this.loads.next(true);
    this._sprintsService.getSprint(this.sprintId).subscribe((res) => {
      this.sprint = res;
      this.sprint.entities;
      this.loads.next(false);
      this._prepareKanban();
    });
  }

  _prepareKanban() {
    const tasks = this.sprint.entities;
    const statuses = new Set(tasks.map((task) => task.status));
    statuses.forEach((status) => {
      this.kanban.push({
        status: status,
        tasks: tasks.filter((task) => task.status === status),
      });
    });

    this.kanban.sort((a, b) => {
      const result = this.priority[a.status] - this.priority[b.status];
      return result;
    });
  }
}
