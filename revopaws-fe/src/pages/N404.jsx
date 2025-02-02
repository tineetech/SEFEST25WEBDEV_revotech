import React from 'react'
import { Link } from 'react-router-dom'

const N404 = () => {
  return (
    <section className="bg-white dark:bg-gray-900">
        <div className="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6">
            <div className="mx-auto max-w-screen-sm justify-center flex flex-col text-center">
            <div className='w-full flex justify-center'>
            </div>
            <div className='w-full flex justify-center text-center align-items-center'>
                <h1 className="flex mb-4 text-7xl tracking-tight font-extrabold lg:text-9xl w-auto text-primary-600 dark:text-primary-500">4
                    <img src="/images/revopaws_logo1.png" alt="logo" className='w-40' />
                    {/* {"0"} */}
                4</h1>
            </div>
            <p className="mb-4 text-3xl tracking-tight font-bold text-gray-900 md:text-4xl dark:text-white">Something's missing.</p>
            <p className="mb-4 text-lg font-light text-gray-500 dark:text-gray-400">Sorry, we can't find that page. You'll find lots to explore on the home page. </p>
            <div>
                <Link to="/" className="inline-flex text-white bg-primary-600 hover:bg-primary-500 hover:text-white focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:focus:ring-primary-900 my-4">Back to Homepage</Link>
            </div>
            </div>   
        </div>
    </section>
  )
}

export default N404