import reflex as rx

from ..components.navbar import navbar

def about():
    """The main view."""
    return rx.container(
        navbar(),
        rx.vstack(
            rx.heading("About this tool"),
            rx.text("""This tool is a simple color palette grenerator from images.
                        You can upload any image from the supported types and get a color palette from the dominant colors of the image.
                    """),
            rx.heading("How it works"),
            rx.text("""As mentioned above, the color palette uses the dominant colors from the image. 
                    k-means clustering is used to extract the dominant colors of the image.
                    
                    """),
            rx.text("""k-means clustering is a method of vector quantization, 
                    originally from signal processing, that aims to partition n observations into k 
                    clusters in which each observation belongs to the cluster with the nearest mean 
                    (cluster centers or cluster centroid), serving as a prototype of the cluster. 
                    This results in a partitioning of the data space into Voronoi cells.
                     k-means clustering minimizes within-cluster variances (squared Euclidean distances), 
                    but not regular Euclidean distances, which would be the more difficult Weber problem: 
                    the mean optimizes squared errors, whereas only the geometric median minimizes Euclidean 
                    distances. For instance, better Euclidean solutions can be found using k-medians and k-medoids."""),

            rx.text("""The problem is computationally difficult (NP-hard); however, efficient heuristic algorithms 
                    converge quickly to a local optimum. These are usually similar to the expectation–maximization 
                    algorithm for mixtures of Gaussian distributions via an iterative refinement approach employed by 
                    both k-means and Gaussian mixture modeling. They both use cluster centers to model the data; however,
                     k-means clustering tends to find clusters of comparable spatial extent, while the Gaussian mixture model 
                    allows clusters to have different shapes."""),


            rx.text("""The unsupervised k-means algorithm has a loose relationship to the k-nearest neighbor classifier, 
                    a popular supervised machine learning technique for classification that is often confused with k-means 
                    due to the name. Applying the 1-nearest neighbor classifier to the cluster centers obtained by k-means 
                    classifies new data into the existing clusters. This is known as nearest centroid classifier or Rocchio algorithm.
                    """),
            rx.link(
                "More Info",
                href="https://en.wikipedia.org/wiki/K-means_clustering",
                is_external=True),
                padding="1em",
                 )
    )