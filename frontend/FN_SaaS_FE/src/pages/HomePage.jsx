import { getBlogs } from "@/services/blogAPI"
import BlogContainer from "../ui_components/BlogContainer"
import Header from "../ui_components/Header"
import { useQuery, keepPreviousData } from "@tanstack/react-query"
import {useState} from 'react'
import PagePagination from "@/ui_components/PagePagination"



const HomePage = () => {
  const [page, setPage] = useState(1);
  const numOfBlogPerPage = 3;

// data: blogs = []
  const {isPending, isError, error, data} = useQuery({
    queryKey: ['blogs', page],
    queryFn: () =>  getBlogs(page),
    placeholderData: keepPreviousData,
  })



  const blogs = data?.results || [];
  const numOfPages = Math.ceil(data?.count / numOfBlogPerPage)

  console.log(blogs)

  function handleSetPage(val) {
    setPage(val)
  }

  function increasePageValue() {
    setPage((curr) => curr + 1);
  }

  function decreasePageValue() {
    setPage((curr) => curr - 1);
  }
  

  console.log(blogs);

  return (
<> 
<Header />
<BlogContainer isPending={isPending} blogs={blogs}/>
<PagePagination
increasePageValue={increasePageValue}
decreasePageValue={decreasePageValue}
page={page}
numOfPages={numOfPages}
handleSetPage={handleSetPage} 
/>

</>  
  )
}

export default HomePage