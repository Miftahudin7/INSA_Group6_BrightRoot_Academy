import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { 
  BookOpenIcon, 
  DocumentTextIcon, 
  ChatBubbleLeftRightIcon,
  AcademicCapIcon,
  ArrowRightIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');

  const features = [
    {
      icon: BookOpenIcon,
      title: 'Study Materials',
      description: 'Access organized textbooks and reference materials from Grade 9 to 12',
      href: '/materials',
      color: 'primary'
    },
    {
      icon: DocumentTextIcon,
      title: 'Past Exam Papers',
      description: 'Browse 10 years of EUEE exam papers with solutions',
      href: '/exams',
      color: 'accent'
    },
    {
      icon: ChatBubbleLeftRightIcon,
      title: 'AI Tutor',
      description: 'Chat with an AI tutor powered by your study materials',
      href: '/chat',
      color: 'success'
    },
    {
      icon: AcademicCapIcon,
      title: 'Upload Your Materials',
      description: 'Upload your own study files for personalized learning',
      href: '/upload',
      color: 'warning'
    }
  ];

  const stats = [
    { label: 'Study Materials', value: '500+' },
    { label: 'Exam Papers', value: '100+' },
    { label: 'Subjects', value: '9' },
    { label: 'Grade Levels', value: '4' }
  ];

  return (
    <>
      <Head>
        <title>EUEE Study Companion - AI-Powered Learning Platform</title>
        <meta name="description" content="AI-Powered Learning Platform for Ethiopian High School Students" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-accent-600 text-white">
          <div className="absolute inset-0 bg-black/10"></div>
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
            <div className="text-center">
              <h1 className="text-4xl md:text-6xl font-bold mb-6">
                EUEE Study Companion
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-primary-100">
                AI-Powered Learning Platform for Ethiopian High School Students
              </p>
              <p className="text-lg mb-12 text-primary-200 max-w-3xl mx-auto">
                Only 2-5% of Ethiopian students pass the EUEE. We're here to change that. 
                Access organized study materials, past exam papers, and chat with an AI tutor.
              </p>
              
              {/* Search Bar */}
              <div className="max-w-2xl mx-auto mb-12">
                <div className="relative">
                  <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search for study materials, exam papers, or topics..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 text-gray-900 rounded-lg border-0 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-primary-600"
                  />
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/materials" className="btn-accent text-lg px-8 py-4">
                  Start Learning
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
                </Link>
                <Link href="/about" className="btn-secondary text-lg px-8 py-4">
                  Learn More
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2">
                    {stat.value}
                  </div>
                  <div className="text-gray-600">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Everything You Need to Succeed
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Our comprehensive platform provides all the tools you need to prepare for the EUEE
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <Link key={index} href={feature.href} className="group">
                  <div className="card hover:shadow-medium transition-all duration-300 group-hover:scale-105">
                    <div className={`inline-flex p-3 rounded-lg bg-${feature.color}-100 text-${feature.color}-600 mb-4`}>
                      <feature.icon className="h-8 w-8" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600">
                      {feature.description}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-primary-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Improve Your EUEE Score?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of students who are already using our platform to prepare for the EUEE
            </p>
            <Link href="/materials" className="btn-accent text-lg px-8 py-4">
              Get Started Today
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </section>
      </main>
    </>
  );
} 