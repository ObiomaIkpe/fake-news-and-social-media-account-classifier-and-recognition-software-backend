import BlogCard from "./BlogCard"
import Spinner from "./Spinner";

const BlogContainer = ({isPending, blogs=[], title="latest posts"}) => {

  console.log("Received blogs:", blogs);

  if(isPending){
    return <Spinner />
  }

  if (!Array.isArray(blogs)) {
    console.log("Unexpected blogs format:", blogs);
    return <p>No blogs available</p>;
}



  return (
    <section className="padding-x py-6  max-container">
    <h2 className="font-semibold text-xl mb-6 dark:text-white text-center">
      {title}
    </h2>
    
    <div className="flex items-center gap-6 justify-center flex-wrap">
      {blogs.map((blog) => <BlogCard key={blog.id} blog={blog}/>)}
    </div>
  </section>
  )
}

export default BlogContainer