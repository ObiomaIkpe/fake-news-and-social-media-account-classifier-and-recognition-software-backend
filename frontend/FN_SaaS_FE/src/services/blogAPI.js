import api from "@/api";


export async function getBlogs(page){
    try {
        const response = await api.get(`blog_list?page=${page}`);
        console.log(response, 'res from api direct');
        return response.data;
    } catch (error) {
        throw new Error(error.message)
    }
}

export async function getBlog(slug) {
    try {
        const response = await api.get(`blogs/${slug}`);
        return response.data;
        
    } catch (error) {
        throw new Error(error.messge)
    }
}

export async function registerUser(data){
    try {
        const response = await api.post("register_user/", data);
        return response.data;
    } catch (error) {
        if (error.status == 400) {
            throw new Error("Username already exists");
          }
          throw new Error(error.message);
        }
} 

export async function signin(data){
    try {
        const response =await api.post("token/", data);
        return response.data
    } catch (error) {
        if (error.status === 401) {
            throw new Error("Invalid Credentials");
          }
      
          throw new Error(error);
        }
}

export async function getUsername(){
    try {
        const response = await api.get("get_username");
        return response.data;
        console.log(response)
    } catch (error) {
        throw new Error(error.message)
    }
}

export async function createBlog(data){
    try {
        const response = await api.post("create_blog/", data);
        return response.data; 
    } catch (err) {
        console.log(err)
        throw new Error(err.message);
    }
}

export async function updateBlog(data, id){
    try {
        const response = await api.put(`update_blog/${id}/`, data);
        return response.data;
    } catch (error) {
        if(error.response){
            throw new Error(error.response?.data?.message || "failed to update blog")
        }
        throw new Error(error.message);
    }
}

export async function deleteBlog(id) {
    try {
        const response = await api.post(`delete_blog/${id}/`);
        return response.data;
    } catch (error) {
        if(error.response){
            throw new Error(error.response?.data?.message || "failed to save blog");
        }
        throw new Error(err.message)
    }
}

export async function getUserInfo(username) {
    try {
        const response = await api.get(`get_userinfo/${username}`);
        return response.data;
    } catch (error) {
        throw new Error(error.message)
    }
}

export async function updateProfile(data) {
    try {
        
    } catch (error) {
        if(error.message){
            throw new Error(error?.response?.data.username[0] || "failed to upload profile");
        }
        throw new Error(error.message);
    }
}