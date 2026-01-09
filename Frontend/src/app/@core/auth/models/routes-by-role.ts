import { Role } from './role.enum';
import { AppRoutes } from './routes.enum';

export const RoutesByRole = [
  {
    role: Role.MEMBER,
    routes: [
      AppRoutes.Home,
      AppRoutes.Assessments,
      AppRoutes.Classes,
      AppRoutes.Logout,
      AppRoutes.CreateAssessment,
      AppRoutes.EditAssessment,
      AppRoutes.AssessmentWritingDetails,
    ],
  },
  {
    role: Role.ADMIN,
    routes: [
      AppRoutes.Account,
      AppRoutes.Users,
      AppRoutes.Assessments,
      AppRoutes.Billing,
      AppRoutes.Students,
      AppRoutes.Settings,
      AppRoutes.Classes,
      AppRoutes.Home,
      AppRoutes.Logout,
      AppRoutes.CreateAssessment,
      AppRoutes.EditAssessment,
      AppRoutes.AssessmentWritingDetails,
    ],
  },
  {
    role: Role.OWNER,
    routes: [
      AppRoutes.Account,
      AppRoutes.Users,
      AppRoutes.Assessments,
      AppRoutes.Billing,
      AppRoutes.Students,
      AppRoutes.Settings,
      AppRoutes.Classes,
      AppRoutes.Home,
      AppRoutes.Logout,
      AppRoutes.CreateAssessment,
      AppRoutes.EditAssessment,
      AppRoutes.AssessmentWritingDetails,
    ],
  },
];
