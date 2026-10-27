import { OrthancProvider, ProjectRepository, ProviderFactory, RepositoryFactory } from "@optica/core"

// Imported first by main.ts: the stores and components get the repository from the factories.
// The backend sends the standard payload: one acquisition, the slices and the stacked images.
ProviderFactory.register("ORTHANC", (url) => new OrthancProvider(url, "stackoptica"))
RepositoryFactory.register("DATA", (provider) => new ProjectRepository(provider))

export function getRepository(): ProjectRepository {
    return RepositoryFactory.get<ProjectRepository>()
}
