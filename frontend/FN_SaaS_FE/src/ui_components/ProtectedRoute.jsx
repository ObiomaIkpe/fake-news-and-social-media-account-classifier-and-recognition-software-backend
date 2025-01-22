import { jwtDecode } from "jwt-decode"
import { useState, useEffect } from "react"
import { Navigate, useLocation } from "react-router-dom";


const ProtectedRoute = ({children}) => {
    const [isAuthourized, setIsAuthorized] = useState(null);
    const location =useLocation();

    useEffect(function() {
        authorize().catch(() => setIsAuthorized(false))
    }, [])

    async function refreshToken() {
        const refresh = localStorage.getItem("refresh")

        try {
            const response = await api.post("token_refresh/", {refresh})
            if(response.status === 200){
                localStorage.setItem("access", response.data.access)
                setIsAuthorized(true)
            }
            else{
                setIsAuthorized(false)
            }
        } catch (error) {
            setIsAuthorized(false)
            console.log(error)
        }
    }

async function authorize() {
    const token = localStorage.getItem("access")
        if(!token){
            setIsAuthorized(false)
            return
        }

        const decodedToken = jwtDecode(token)
        const expiry_date = decodedToken.exp
        const current_time = Date.now()/1000

        if(current_time > expiry_date){
            await refreshToken()
        } else {
            setIsAuthorized(true)
        }   
}

if (isAuthourized === null){
    return <h1>please log in!</h1>
}


  return (
    <>
    {isAuthourized ? children : <Navigate to="/signin" state={{from:location}} replace/>}
    </>
  )
}

export default ProtectedRoute