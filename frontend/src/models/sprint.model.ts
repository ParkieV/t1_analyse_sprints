export interface Sprint {
  id: string; // '6738497cd0abd6989076bcd9';
  sprintName: string; // 'Спринт 2024.3.1.NPP Shared Sprint';
  sprintStatus: SprintStatus;
  sprintStartDate: string; // '2024-07-03T19:00:00';
  sprintEndDate: string; // '2024-07-16T19:00:00';
  entityIds: number[];
}

export type SprintStatus = 'Закрыт' | string;
