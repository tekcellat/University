using UnityEngine;
using System.Collections;
using UnityEngine.UI;
public class hamadaController : MonoBehaviour
{
    public float speed = 5;
    public bool flipped = false;
    public Vector2 vel;
    public float max_rot_angle;
    public GameObject winMessage;
    public int rotationconstant = 20;

    // Use this for initialization
    void Start()
    {
        max_rot_angle = .4f;

    }

    // Update is called once per frame
    void Update()
    {
        Camera.main.transform.position = this.transform.position + new Vector3(0, 0, -10);
        float zRotation = Input.GetAxis("Vertical");
        vel = transform.right;
        if (flipped)
        {
            zRotation = -zRotation;
        }
        gameObject.transform.Rotate(new Vector3(0, 0, zRotation));
    }
    void FixedUpdate()
    {
        this.rigidbody2D.velocity = transform.right * speed;// *speed;
        this.rigidbody2D.angularVelocity = 0;
    }
    void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.tag == "Mirror")
        {
            Debug.Log(transform.rotation.eulerAngles);
            if (vel.y < 0)
                this.transform.Rotate(new Vector3(0, 0, 45 - transform.rotation.eulerAngles.z));
            else
                this.transform.Rotate(new Vector3(0, 0, -45));
            //this.transform.rotation= Quaternion.Euler(0,0,-45+this.transform.rotation.eulerAngles.z);
            flipped = !flipped;
        }
        else
        {
            GameObject koto=Object.Instantiate(winMessage) as GameObject;
            koto.transform.GetChild(0).GetComponent<Text>().text = "You Lose";
            Destroy(gameObject);
        }
    }
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.tag == "Win")
        {
            GameObject koto = Object.Instantiate(winMessage) as GameObject;
            koto.transform.GetChild(0).GetComponent<Text>().text = "You Win ya Loser";
            Destroy(gameObject);
        }
        else{
            this.gameObject.transform.Rotate(0, 0, rotationconstant * Mathf.Cos(this.transform.rotation.eulerAngles.z * Mathf.Deg2Rad));
        }
    }

}
