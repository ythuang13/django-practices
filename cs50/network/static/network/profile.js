document.addEventListener('DOMContentLoaded', () => {

    const follow_link = document.getElementById('follow_link');
    if (follow_link !== null) {
        follow_link.addEventListener('click', follow_or_unfollow);
    }
});

function follow_or_unfollow(event) {
    event.preventDefault();
    const user_id = this.dataset.user_id;

    fetch(`./${user_id}/follow`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': this.dataset.csrf
        }
    })
    .then(response => response.json())
    .then(result => {
        const follow_link = document.getElementById('follow_link');
        follow_link.innerText = (follow_link.innerText === "unfollow") ? "follow" : "unfollow";
    })
    .catch(error => {
        console.log("Error: ", error);
    });

    return false;
}