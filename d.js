const url = 'https://api.themoviedb.org/3/movie/now_playing?api_key=a07e22bc18f5cb106bfe4cc1f83ad8ed'
const fetch_ = async () => {
    try {
        const res = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        })
        const json = res.json()
        console.log(json)
    }
    catch(e){
        console.log(e)
    }
}
fetch_()