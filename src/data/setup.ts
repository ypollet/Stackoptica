import { coreProviders, createProvider, ProjectRepository, type Acquisition, type Coords3D, type ProjectImage } from "optica-core"

// Imported first by main.ts. The backend is the one of the environment (.env: VITE_BACKEND_TYPE, VITE_BACKEND_URL).
// The backend sends the standard payload: one acquisition, the slices and the stacked images, and 3D positions.
type StackRepository = ProjectRepository<ProjectImage, Acquisition<ProjectImage>, Coords3D>
const repository: StackRepository = new ProjectRepository(createProvider(coreProviders("stackoptica")))

export function getRepository(): StackRepository {
    return repository
}
