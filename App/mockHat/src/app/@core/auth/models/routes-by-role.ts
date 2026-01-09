import { Role } from './role.enum';
import { AppRoutes } from './routes.enum';

export const RoutesByRole = [
  {
    role: Role.Student,
    routes: [
      AppRoutes.DashBoard,
      AppRoutes.Writing,
      AppRoutes.Payments,
      AppRoutes.Info,
      AppRoutes.Plans,
    ],
  },
  {
    role: Role.Teacher,
    routes: [
      AppRoutes.DashBoard,
      AppRoutes.Writing,
      AppRoutes.Payments,
      AppRoutes.Info,
      AppRoutes.Plans,
      AppRoutes.Students,
    ],
  },
  {
    role: Role.Administrator,
    routes: [
      AppRoutes.DashBoard,
      AppRoutes.Users,
      AppRoutes.Payments,
      AppRoutes.AssessmentQuestion,
      AppRoutes.Writing,
      AppRoutes.Info,
      AppRoutes.Plans,
      AppRoutes.Students,
    ],
  },
];
