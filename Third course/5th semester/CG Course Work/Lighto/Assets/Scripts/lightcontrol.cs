using UnityEngine;
using System.Collections;

public class lightcontrol : MonoBehaviour
{
    public float speed;
    public float max_rot_angle;
	// Use this for initialization
	void Start () {
	  
	}
	
	// Update is called once per frame
	void Update () {
        float zRotation = Input.GetAxis("Horizontal");
        if (transform.rotation.z < -max_rot_angle)
        {
            
            if(zRotation > 0)
                gameObject.transform.Rotate(new Vector3(0, 0, zRotation));
        }
        else if (transform.rotation.z > max_rot_angle)
        {
            
            if (zRotation < 0)
                gameObject.transform.Rotate(new Vector3(0, 0, zRotation));
        }
        else
        {
            
            gameObject.transform.Rotate(new Vector3(0, 0, zRotation));
        }
        
        this.rigidbody2D.velocity = this.transform.right * speed;
	}
    
    void FixedUpdate()
    {
        
    }
}
